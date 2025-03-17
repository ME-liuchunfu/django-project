import logging

from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from common.utils import is_not_empty, keys_to_camel, keys_to_snake
from system.models import SysMenu
from system.serializers.models import SysMenuSerializer
from system.user.permission_services import ADMIN_USER_ID

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class MenuService:
    """
    菜单
    """

    def menu_list(self, params=None, user_id: int = -1) -> list[dict]:
        ret_datas = []
        q = Q()
        if params is None:
            params = {}

        query_data = []
        sql_params = []

        if params.get("menuName") and is_not_empty(params.get("menuName")):
            q = q & Q(menu_name__icontains=params["menuName"].strip())
            query_data.append(params["menuName"].strip())
            sql_params.append("m.menu_name like concat('%', %s, '%')")
        if params.get("visible") and is_not_empty(params.get("visible")):
            q = q & Q(visible=params["visible"].strip())
            query_data.append(params["visible"].strip())
            sql_params.append("m.visible = %s")
        if params.get("status") and is_not_empty(params.get("status")):
            q = q & Q(status=params["status"].strip())
            query_data.append(params["status"].strip())
            sql_params.append("m.status = %s")

        if ADMIN_USER_ID != user_id:
            query_params = []
            query_params.append(user_id)
            sql = """
                select distinct m.menu_id, m.parent_id, m.menu_name, m.path, m.component, m.`query`, m.route_name, m.visible, m.status, ifnull(m.perms,'') as perms, m.is_frame, m.is_cache, m.menu_type, m.icon, m.order_num, m.create_time
                from sys_menu m
                left join sys_role_menu rm on m.menu_id = rm.menu_id
                left join sys_user_role ur on rm.role_id = ur.role_id
                left join sys_role ro on ur.role_id = ro.role_id
                where 
            """
            sql_params.insert(0, " ur.user_id = %s ")
            sql = f"{sql} {' AND '.join(sql_params)}  order by m.parent_id, m.order_num "
            query_params.extend(query_data)
            menu_datas = SysMenu.objects.raw(sql, query_params)
        else:
            menu_datas = SysMenu.objects.filter(q).order_by('parent_id', 'order_num').all()

        if menu_datas and len(menu_datas) > 0:
            for menu_data in menu_datas:
                data = SysMenuSerializer(menu_data).data
                data.update({"children": []})
                ret_datas.append(keys_to_camel(data))

        return ret_datas

    def build_menu_treeselect(self, datas: list) -> list[dict]:
        """
        菜单下拉树
        """
        res_datas = []
        temp_list = [menu.get('menuId') for menu in datas]

        for data in datas:
            parent_id = data.get('parentId')
            if parent_id not in temp_list:
                self.__recursion_fn(datas, data)
                res_datas.append(data)
                pass
        if len(temp_list) == 0:
            res_datas = datas

        res_datas = self.to_menu_select_tree(res_datas)
        return res_datas

    def __recursion_fn(self, datas: list, data: dict):
        """
        递归列表
        """
        child_list = self.__get_child_list(datas, data)
        data['children'] = child_list
        for child in child_list:
            if self.__has_child(datas, child):
                self.__recursion_fn(datas, child)

    def __has_child(self, datas, child) -> bool:
        n_list = self.__get_child_list(datas=datas, t=child)
        return len(n_list) > 0

    def __get_child_list(self, datas: list[dict], t: dict) -> list:
        t_datas = []
        for n in datas:
            if n.get('parentId') == t.get('menuId'):
                t_datas.append(n)
        return t_datas

    def to_menu_select_tree(self, datas: list) -> list[dict]:
        res_datas = []
        for data in datas:
            res_datas.append(self.build_menu_tree_dict(data))
        return res_datas

    def build_menu_tree_dict(self, menu: dict) -> dict:
        children = menu.get('children')
        data = {
            'id': menu.get('menuId'),
            'label': menu.get('menuName'),
            'children': [],
        }
        if children and len(children) > 0:
            c_list = []
            for child in children:
                c_list.append(self.build_menu_tree_dict(child))
            data['children'].extend(c_list)
        return data

    def menu(self, menu_id: int) -> dict:
        data = SysMenu.objects.get(menu_id=menu_id)
        if data:
            data = keys_to_camel(SysMenuSerializer(data).data)
        else:
            data = {}
        return data

    def del_menu(self, menu_id: int) -> int:
        try:
            row, _s = SysMenu.objects.filter(menu_id=menu_id).delete()
        except Exception as e:
            row = 0
            logger.error(f'[删除菜单失败],menu_id:{menu_id}', exc_info=True)
        return row

    def update_menu(self, menu: dict, user_id: int, user_name: str) -> int:
        try:
            menu = keys_to_snake(menu)
            update_dict = {}
            if not menu.get('menu_id'):
                raise ValueError("参数错误")

            read_only_keys = ['create_by', 'create_time', 'menu_id', 'update_time']
            for key, value in menu.items():
                if key in read_only_keys:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            row = SysMenu.objects.filter(menu_id=menu.get('menu_id')).update(**update_dict)
        except Exception as e:
            row = 0
            logger.error(f'[更新菜单异常],menu:{menu}', exc_info=True)

        return row

    def add_menu(self, menu_dict:dict, user_id:int, user_name: str) -> int:
        try:
            add_dict = keys_to_snake(menu_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()
            sys_menu = SysMenu(**add_dict)
            sys_menu.save()
            row = 1
        except Exception as e:
            row = 0
            logger.error(f'[新增菜单异常], menu: {menu_dict}', exc_info=True)

        return row

