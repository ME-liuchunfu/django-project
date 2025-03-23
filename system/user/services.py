import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone

from common.cryption.cryption import bcrypt_hash_password
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns, sql_date_parse, del_int_column_key, sql_order_by_parse
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.dept.services import DeptService
from system.models import SysUser
from system.post.services import PostService
from system.role.services import RoleService, UserRoleService
from system.serializers.models import SysUserSerializer
from django.conf import settings

from system.user.permission_services import is_admin
from system.userpost.services import UserPostService

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class UserService:

    def search_key_handler(self, k):
        if k in ['title', 'oper_ip', 'oper_name']:
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def get_time_columns(self):
        return {
            'login_time': {
                "convert": sql_date_parse,
                "format": "%Y-%m-%d %H:%M:%S",
                "val": ['params[begin_time]', 'params[end_time]']
            },
        }

    def user_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            parse_page_result = ParsePageResult()
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            order_columns = sql_order_by_parse(req_data=req_data, default_vals=['user_id'])
            query_set = SysUser.objects.filter(**sql_params_dict).order_by(*order_columns).all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            res_page = parse_page_result(data_query_set=query_set)
            self.__inject_query_page_Info(res_page)
            return res_page
        except Exception as e:
            logger.error(f'[查询用户列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysUser) -> Any | None:
        try:
            res = keys_to_camel(SysUserSerializer(data).data)
            res['userName'] = res['username']
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def user_info(self, user_id: int = None) -> dict:
        res_data = {}
        try:
            if user_id:
                data = SysUser.objects.filter(user_id=user_id).get()
                res_data['data'] = self.serializer_model(data)
                res_data['postIds'] = UserPostService().post_list_by_user_id(user_id=data.user_id)
                role_ids, _ = UserRoleService().role_ids_in_user_ids(user_ids=[data.user_id])
                res_data['roleIds'] = list(role_ids)

            roles = RoleService().role_all()
            if user_id and  not is_admin(user_id):
                roles = [role for role in roles if not is_admin(role.get('roleId'))]

            res_data['roles'] = roles
            res_data['posts'] = PostService().post_all()
        except Exception as e:
            logger.error(f'[查询用户信息]异常, user_id: {user_id}', exc_info=True)
        return res_data

    def del_user(self, user_ids: list[int]) -> int:
        try:
            row, _ = SysUser.objects.filter(user_id__in=user_ids).delete()
            return row
        except Exception as e:
            logger.error(f'[删除用户信息]异常, user_ids: {user_ids}', exc_info=True)
            return 0

    def add_user(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['username'] = add_dict['user_name']
            add_dict['del_flag'] = 0
            add_dict['user_type'] = '00'
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()

            post_ids = req_dict.get('postIds')
            role_ids = req_dict.get('roleIds')

            if not add_dict.get('user_name'):
                return -1, '账号不能为空'
            # 1、先判断用户是否存在， 是否唯一键
            query_set = SysUser.objects.filter(username=add_dict.get('user_name')).all()
            if query_set and len(query_set) > 0:
                return -1, f"新增用户'{add_dict.get('user_name')}'失败，登录账号已存在"

            # 2、手机号
            if add_dict.get('phonenumber'):
                query_set = SysUser.objects.filter(phonenumber=add_dict.get('phonenumber')).all()
                if query_set and len(query_set) > 0:
                    return -1, f"新增用户'{add_dict.get('user_name')}'失败，手机号已存在"

            # 3、邮箱
            if add_dict.get('email'):
                query_set = SysUser.objects.filter(email=add_dict.get('email')).all()
                if query_set and len(query_set) > 0:
                    return -1, f"新增用户'{add_dict.get('user_name')}'失败，邮箱号已存在"

            all_columns = get_model_fields_name(SysUser)
            del_not_model_key(add_dict, all_columns)
            add_dict['password'] = bcrypt_hash_password(add_dict.get('password'))
            sys_user = SysUser(**add_dict)
            sys_user.save()
            if post_ids and len(post_ids) > 0:
                UserPostService().insert_user_post(user_id=sys_user.user_id, post_ids=post_ids)

            if role_ids and len(role_ids) > 0:
                UserRoleService().insert_user_role(user_id=sys_user.user_id, role_ids=role_ids)

            return 1, None
        except Exception as e:
            logger.error(f'[新增用户信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_user(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            user = keys_to_snake(req_dict)
            update_dict = {}
            if not user.get('user_id'):
                return -1, "参数错误"

            post_ids = req_dict.get('postIds')
            role_ids = req_dict.get('roleIds')

            if is_admin(user.get('user_id')):
                return -1, '不允许操作超级管理员'

            if not user.get('user_name'):
                return -1, '账号不能为空'
            # 1、先判断用户是否存在， 是否唯一键
            query_set = SysUser.objects.filter(username=user.get('user_name')).exclude(user_id=user.get('user_id')).all()
            if query_set and len(query_set) > 0:
                return -1, f"更新用户'{user.get('user_name')}'失败，登录账号已存在"

            # 2、手机号
            if user.get('phonenumber'):
                query_set = SysUser.objects.filter(phonenumber=user.get('phonenumber')).exclude(user_id=user.get('user_id')).all()
                if query_set and len(query_set) > 0:
                    return -1, f"更新用户'{user.get('user_name')}'失败，手机号已存在"

            # 3、邮箱
            if user.get('email'):
                query_set = SysUser.objects.filter(email=user.get('email')).exclude(user_id=user.get('user_id')).all()
                if query_set and len(query_set) > 0:
                    return -1, f"更新用户'{user.get('user_name')}'失败，邮箱号已存在"

            all_columns = get_model_fields_name(SysUser)
            read_only_keys = ['create_by', 'create_time', 'user_id', 'update_time', 'password']
            for key, value in user.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            all_columns = get_model_fields_name(SysUser)
            del_not_model_key(update_dict, all_columns)
            # 1、先删除角色 & 建立新的角色
            UserRoleService().del_user_role(user.get('user_id'))
            if role_ids and len(role_ids) > 0:
                UserRoleService().insert_user_role(user.get('user_id'), role_ids=role_ids)
            # 2、先删除岗位 & 建立新的岗位
            UserPostService().del_user_post(user.get('user_id'))
            if post_ids and len(post_ids) > 0:
                UserPostService().insert_user_post(user.get('user_id'), post_ids=post_ids)

            row = SysUser.objects.filter(user_id=user.get('user_id')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新用户异常],req_dict:{req_dict}', exc_info=True)
            return -1, '更新用户异常'

        return row, None

    def export_user(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            order_columns = sql_order_by_parse(req_data=req_data, default_vals=['user_id'])
            query_set = SysUser.objects.filter(**sql_params_dict).order_by(*order_columns).all()
            response = ResponseStream().query_set_to_excel_http_response(name="用户信息", query_set=query_set, time_fields=['login_time'])
            return response
        except Exception as e:
            logger.error(f'[导出用户信息]异常')
            raise ValueError('导出用户信息异常') from e

    def __inject_query_page_Info(self, page_result: PageResult):
        if page_result and len(page_result.rows) > 0:
            dept_ids = set([row.get("deptId") for row in page_result.rows])
            user_ids = set([row.get("userId") for row in page_result.rows])
            res_depts = DeptService().dept_info_in_ids(dept_ids=dept_ids)
            role_ids, user_role_dict = UserRoleService().role_ids_in_user_ids(user_ids=user_ids)
            res_roles = RoleService().role_info_in_ids(role_ids=role_ids)

            for row in page_result.rows:
                row['dept'] = res_depts.get(row.get("deptId"))
                roles = []
                row['roles'] = roles
                user_role_ids = user_role_dict.get(row.get("userId"))
                if user_role_ids:
                    for user_role_id in user_role_ids:
                        role = res_roles.get(user_role_id)
                        if role:
                            roles.append(role)



