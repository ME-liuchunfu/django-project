import logging
import re
from typing import Any

from django.http import HttpResponse
from django.utils import timezone

from common.data_frame import inject_sql_params_dict, ParsePageResult, inject_page_params, PageResult, \
    get_model_fields_name, del_not_model_key
from common.http import ResponseStream
from common.utils import keys_to_camel, keys_to_snake
from system.models import SysDept
from system.serializers.models import SysDeptSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class DeptService:

    def dept_list_by_role_id(self, role_id: int, dept_check_strictly: int) -> list:
        try:
            sql_params = []
            sql = """
                select d.dept_id
                from sys_dept d
                    left join sys_role_dept rd on d.dept_id = rd.dept_id
                where rd.role_id = %s 
            """
            sql_params.append(role_id)
            sub = " "
            if dept_check_strictly == 1:
                sub = """
                and d.dept_id not in (select d.parent_id from sys_dept d inner join sys_role_dept rd on d.dept_id = rd.dept_id and rd.role_id = %s
                """
                sql_params.append(role_id)

            sql = f"{sql} {sub} order by d.parent_id, d.order_num"
            query_set = SysDept.objects.raw(sql, sql_params)
            if query_set and len(query_set) > 0:
                res_list = []
                for data in query_set:
                    res_list.append(keys_to_camel(SysDeptSerializer(data).data))
                return res_list
        except Exception as e:
            logger.error(f'[查询部门角色异常], role_id:{role_id}, dept_check_strictly:{dept_check_strictly}',
                         exc_info=True)

        return []

    def search_key_handler(self, k):
        if k == 'dept_name':
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def dept_tree_list(self, params_dict: dict) -> list:
        try:
            req_data = keys_to_snake(params_dict)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            sql_params_dict['del_flag'] = '0'
            query_set = SysDept.objects.filter(**sql_params_dict).order_by('parent_id', 'order_num').all()
            if query_set and len(query_set) > 0:
                res_list = []
                for data in query_set:
                    res_list.append(keys_to_camel(SysDeptSerializer(data).data))
                return res_list
        except Exception as e:
            logger.error(f'[查询部门tree]异常, params_dict:{params_dict}', exc_info=True)

        return []

    def build_dept_tree(self, dept_list: list[dict]) -> list:
        res_list = []
        temp_list = [dept.get('deptId') for dept in dept_list]
        for dept in dept_list:
            if dept.get('parentId') not in temp_list:
                self.__recursion_fn(dept_list, dept)
                res_list.append(dept)

        if len(res_list) == 0:
            res_list = dept_list

        res_list = self.__build_dept_tree_select(res_list)
        return res_list

    def __recursion_fn(self, dept_list: list[dict], dept: dict):
        child_list = self.__get_child_list(dept_list, dept)
        dept['children'] = child_list
        for child in child_list:
            if self.__has_child(dept_list, child):
                self.__recursion_fn(dept_list, child)

    def __get_child_list(self, dept_list: list[dict], t: dict) -> list:
        t_list = []
        for n in dept_list:
            if n.get('parentId') is not None and n.get('parentId') == t.get("deptId"):
                t_list.append(n)

        return t_list

    def __has_child(self, dept_list: list[dict], child: dict) -> bool:
        return len(self.__get_child_list(dept_list=dept_list, t=child)) > 0

    def __build_dept_tree_select(self, data_list: list[dict]) -> list:
        res_list = []
        for data in data_list:
            d = self.__build_tree(data)
            res_list.append(d)

        return res_list

    def __build_tree(self, data: dict) -> dict:
        res_dict = {
            "id": data.get('deptId'),
            "label": data.get('deptName'),
            "children": []
        }
        children = data.get('children')
        if children and len(children) > 0:
            for child in children:
                res_dict['children'].append(self.__build_tree(child))
        return res_dict

    def dept_list(self, req_data: dict) -> list:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            query_set = SysDept.objects.filter(**sql_params_dict).order_by("dept_id").all()
            res_datas = []
            if query_set and len(query_set) > 0:
                for data in query_set:
                    dt = self.serializer_model(data)
                    dt['children'] = []
                    res_datas.append(dt)
            return res_datas
        except Exception as e:
            logger.error(f'[查询部门列表异常], req_data: {req_data}', exc_info=True)
            return []

    def serializer_model(self, data: SysDept) -> Any | None:
        try:
            return keys_to_camel(SysDeptSerializer(data).data)
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def dept_info(self, dept_id: int) -> dict:
        res_data = {}
        try:
            datas = SysDept.objects.filter(dept_id=dept_id)
            if datas.exists():
                res_data = self.serializer_model(datas.first())
        except Exception as e:
            logger.error(f'[查询部门信息]异常, dept_id: {dept_id}', exc_info=True)
        return res_data

    def del_dept(self, dept_id: int) -> int:
        try:
            row, _ = SysDept.objects.filter(dept_id=dept_id).delete()
            return row
        except Exception as e:
            logger.error(f'[删除部门信息]异常, dept_id: {dept_id}', exc_info=True)
            return 0

    def add_dept(self, user_id: int, user_name: str, req_dict: dict) -> int:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()
            sys_post = SysDept(**add_dict)
            sys_post.save()
            return 1
        except Exception as e:
            logger.error(f'[新增部门信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}', exc_info=True)
            return 0

    def update_dept(self, user_id: int, user_name: str, req_dict: dict) -> int:
        try:
            params_dict = keys_to_snake(req_dict)
            update_dict = {}
            if not params_dict.get('dept_id'):
                raise ValueError("参数错误")

            all_columns = get_model_fields_name(SysDept)
            read_only_keys = ['create_by', 'create_time', 'dept_id', 'update_time']
            for key, value in params_dict.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            row = SysDept.objects.filter(dept_id=params_dict.get('dept_id')).update(**update_dict)
        except Exception as e:
            row = 0
            logger.error(f'[更新部门异常],req_dict:{req_dict}', exc_info=True)

        return row

    def export_dept(self, req_data : dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            query_set = SysDept.objects.filter(**sql_params_dict).order_by("dept_id").all()
            response = ResponseStream().query_set_to_excel_http_response(name="部门信息", query_set=query_set)
            return response
        except Exception as e:
            logger.error(f'[导出部门信息]异常')
            raise ValueError('导出部门信息异常') from e

    def exclude_dept_list(self, dept_id: int, req_dict: dict) -> list:
        """
        查询部门列表（排除节点）
        """
        res_datas = []
        try:
            sql_params_dict = keys_to_snake(req_dict)
            all_columns = get_model_fields_name(SysDept)
            del_not_model_key(sql_params_dict, all_columns)
            query_set = SysDept.objects.filter(**sql_params_dict).all()
            if query_set and len(query_set) > 0:
                for data in query_set:
                    dt = self.serializer_model(data)
                    if dt.get('dept_id') == dept_id or (dt.get('ancestors') and (str(dept_id) in dt.get('ancestors').split(','))):
                        continue
                    dt['children'] = []
                    res_datas.append(dt)
        except Exception as e:
            logger.error(f'[查询部门-排除节点]错误, dept_id:{dept_id}, req_dict:{req_dict}', exc_info=True)

        return res_datas

    def dept_info_in_ids(self, dept_ids: tuple | list | set = None) -> dict:
        res_datas = []
        try:
            if dept_ids:
                query_set = SysDept.objects.filter(dept_id__in=dept_ids).all()
                if query_set and len(query_set) > 0:
                    for data in query_set:
                        dt = self.serializer_model(data)
                        res_datas.append(dt)
        except Exception as e:
            logger.error(f'[查询部门-指定部门id]错误, dept_ids:{dept_ids}', exc_info=True)

        res_dict = {}
        if res_datas:
            for data in res_datas:
                res_dict[data['deptId']] = data
        return res_dict
