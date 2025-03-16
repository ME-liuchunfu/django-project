import logging
import re

from common.data_frame import inject_sql_params_dict
from common.utils import keys_to_camel, keys_to_snake
from system.models import SysDept
from system.serializers.models import SysDeptSerializer

logger = logging.getLogger(__name__)


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