import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    parse_sql_columns, get_model_fields_name, del_not_model_key
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.dept.services import DeptService
from system.models import SysRole, SysRoleMenu
from system.rolemenu.services import RoleMenuService
from system.serializers.models import SysRoleSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class RoleService:

    def search_key_handler(self, k):
        if k == 'role_name' or k == 'role_key':
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def role_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            sql_params_dict['del_flag'] = '0'
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            parse_page_result = ParsePageResult()
            query_set = SysRole.objects.filter(**sql_params_dict).order_by("role_id").all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询角色列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysRole) -> Any | None:
        try:
            return keys_to_camel(SysRoleSerializer(data).data)
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def role_info(self, role_id: int) -> dict:
        res_data = {}
        try:
            data = SysRole.objects.filter(role_id=role_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询角色信息]异常, role_id: {role_id}', exc_info=True)
        return res_data

    def del_role(self, role_ids: list[int]) -> int:
        try:
            row, _ = SysRole.objects.filter(role_id__in=role_ids).delete()
            # 删除角色菜单
            for role_id in role_ids:
                RoleMenuService().del_role_menus(role_id)
            return row
        except Exception as e:
            logger.error(f'[删除角色信息]异常, role_ids: {role_ids}', exc_info=True)
            return 0

    def add_role(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            all_columns = get_model_fields_name(SysRole)
            add_dict = keys_to_snake(req_dict)
            if self.is_admin(add_dict.get('role_id')):
                return -1, '不允许操作超级管理员'
            # 判断 role_key 是否存在
            key_role = SysRole.objects.filter(role_key=add_dict['role_key']).all()
            if key_role and len(key_role) > 0:
                return -1, '角色权限已存在'
            key_name = SysRole.objects.filter(role_name=add_dict['role_name']).all()
            if key_name and len(key_name) > 0:
                return -1, '角色名称已存在'
            add_dict['create_by'] = user_name
            add_dict['del_flag'] = '0'
            add_dict['create_time'] = timezone.now()
            del_not_model_key(params_dict=add_dict, all_columns=all_columns)
            sys_role = SysRole(**add_dict)
            sys_role.save()
            # 插入角色菜单
            row = self.add_role_menus(role_id=sys_role.role_id, req_dict=keys_to_snake(req_dict))
            return row, None
        except Exception as e:
            logger.error(f'[新增角色信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}', exc_info=True)
            return 0, '新增角色错误'

    def add_role_menus(self, role_id: int, req_dict: dict) -> int:
        menu_ids = req_dict.get('menu_ids')
        data_list: list[SysRoleMenu] = []
        for menu_id in menu_ids:
            menu_dict = {
                "menu_id": menu_id,
                "role_id": role_id,
            }
            data_list.append(SysRoleMenu(**menu_dict))

        if len(data_list) > 0:
            row = RoleMenuService().batch_role_menu(role_menus=data_list)
        else:
            row = 1

        return row

    def update_role(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            update_dict = keys_to_snake(req_dict)
            if not update_dict.get('role_id'):
                raise ValueError("参数错误")

            if self.is_admin(update_dict.get('role_id')):
                return -1, '不允许操作超级管理员'

            # 判断 role_key 是否存在
            key_role = SysRole.objects.filter(role_key=update_dict['role_key']).all()
            if key_role and len(key_role) > 0 and key_role[0].role_id != update_dict['role_id']:
                return -1, '角色权限已存在'
            key_name = SysRole.objects.filter(role_name=update_dict['role_name']).all()
            if key_name and len(key_name) > 0 and key_name[0].role_id != update_dict['role_id']:
                return -1, '角色名称已存在'

            all_columns = get_model_fields_name(SysRole)
            read_only_keys = ['create_by', 'create_time', 'role_id', 'update_time']
            for key, value in req_dict.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            del_not_model_key(params_dict=update_dict, all_columns=all_columns)
            row = SysRole.objects.filter(role_id=update_dict.get('role_id')).update(**update_dict)
            # 更新菜单
            RoleMenuService().del_role_menus(role_id=update_dict.get('role_id'))
            row = self.add_role_menus(role_id=update_dict.get('role_id'), req_dict=keys_to_snake(req_dict))
        except Exception as e:
            row = 0
            logger.error(f'[更新角色异常],req_dict:{req_dict}', exc_info=True)

        return row, None

    def export_role(self, req_data : dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            sql_params_dict['del_flag'] = '0'
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            query_set = SysRole.objects.filter(**sql_params_dict).order_by("role_id").all()
            response = ResponseStream().query_set_to_excel_http_response(name="角色信息", query_set=query_set)
            return response
        except Exception as e:
            logger.error(f'[导出角色信息]异常')
            raise ValueError('导出角色信息异常') from e

    def is_admin(self, role_id: int = None) -> bool:
        if role_id is None:
            return False
        return role_id == 1

    def change_status(self, req_dict: dict) -> dict:
        res_dict = {}
        try:
            req_dict = keys_to_snake(req_dict)
            if not req_dict.get('role_id') or not req_dict.get('status'):
                res_dict['msg'] = "参数错误"
                res_dict['code'] = 500

            if self.is_admin(req_dict.get('role_id')):
                res_dict['msg'] = "不允许操作超级管理员"
                res_dict['code'] = 500
            SysRole.objects.filter(role_id=req_dict.get('role_id')).update(status=req_dict.get('status'))
        except Exception as e:
            logger.error(f'[状态变更错误], req_dict:{req_dict}', exc_info=True)
            res_dict['msg'] = "状态变更错误"
            res_dict['code'] = 500

        return res_dict

    def dept_tree(self, role_id:int) -> dict:
        sys_role = SysRole.objects.filter(role_id=role_id).get()
        keys = DeptService().dept_list_by_role_id(role_id=sys_role.role_id, dept_check_strictly=sys_role.dept_check_strictly)
        dept_list = DeptService().dept_tree_list(params_dict={})
        depts = DeptService().build_dept_tree(dept_list)
        res_dict = {
            "checkedKeys": keys,
            "depts": depts
        }
        return res_dict