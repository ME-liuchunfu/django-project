from typing import Tuple

from system.models import SysRole, SysMenu
from system.serializers.models import SysMenuSerializer

ADMIN_USER = "admin"
ADMIN_USER_ID = 1

ADMIN_PERMISSION = "*:*:*"


class MetaVo:

    def __init__(self, data: dict = None):
        self.data = {
            'title': None,
            'icon': None,
            'noCache': True,
            'link': None,
        }
        if data:
            self.data.update(data)

    def __setattr__(self, key, value):
        self.__setattr__(key, value)

    def __getattr__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return self.data.__str__()

    def __call__(self):
        return self.data


class RouterVo:

    def __init__(self, data: dict = None):
        self.data = {
            'name': None,
            'path': None,
            'hidden': True,
            'redirect': 'noRedirect',
            'component': '',
            'query': None,
            'alwaysShow': False,
            'meta': MetaVo(),
            'children': []
        }
        if data:
            self.__setattr__('name', data.get('name'))
            self.__setattr__('path', data.get('path'))
            self.__setattr__('hidden', data.get('hidden'))
            self.__setattr__('redirect', data.get('redirect'))
            self.__setattr__('component', data.get('component'))
            self.__setattr__('query', data.get('query'))
            self.__setattr__('alwaysShow', data.get('alwaysShow'))
            self.__setattr__('meta', data.get('meta'))
            if 'hidden' in data and not isinstance(data.get('hidden'), bool):
                self.data['hidden'] = data.get('hidden') == '1'


    def set_meta(self, meta: MetaVo):
        self.__setattr__('meta', meta)


    def __setattr__(self, key, value):
        self.__setattr__(key, value)


    def __getattr__(self, item):
        return self.__getattr__(item)


    def __str__(self):
        return self.data.__str__()


    def __call__(self):
        return self.data



def get_routers(user_id:int) -> list:
    if ADMIN_USER_ID == user_id:
        menus_list = __get_menu_tree_all()
    else:
        menus_list = __get_menu_tree_by_user_id(user_id)

    tree_datas = build_tree_menus(menus_list)
    return tree_datas


def build_tree_menus(menus_list: list) -> list:
    tree_datas = []
    for menu in menus_list:
        router_vo = RouterVo(menu)

        tree_datas.append(router_vo)

    return tree_datas


def get_role_permission(user_id: int, username: str) -> tuple[str]:
    if ADMIN_USER == username:
        return (ADMIN_USER,)
    else:
        tuple_data = tuple()
        roles = __get_role_permission(user_id)
        if roles and len(roles) > 0:
            tuple_data = tuple([role.role_key for role in roles if role])
        return tuple_data


def get_menu_permission(user_id: int, username: str, roles: tuple[str] = None) -> tuple:
    if ADMIN_USER == username:
        return (ADMIN_PERMISSION,)
    else:
        if roles and len(roles) > 0:
            list_data = []
            for role in roles:
                data = __get_memu_permission_by_role_name(role)
                list_data.extend(data)
            return tuple(list_data)
        else:
            return __get_memu_permission_by_user_id(user_id)


def __get_menu_tree_all() -> list:
    """
    获取所有菜单
    :return: 菜单集合
    """
    menus = SysMenu.objects.raw("""
        select distinct m.menu_id, m.parent_id, m.menu_name, m.path, m.component, m.`query`, m.route_name, m.visible, m.status, ifnull(m.perms,'') as perms, m.is_frame, m.is_cache, m.menu_type, m.icon, m.order_num, m.create_time
		from sys_menu m where m.menu_type in ('M', 'C') and m.status = 0
		order by m.parent_id, m.order_num
    """)
    if menus and len(menus) > 0:
        menus_data = []
        for menu in menus:
            menus_data.append(SysMenuSerializer(menu).data)
        return menus_data

    return []


def __get_menu_tree_by_user_id(user_id: int) -> list:
    """
    根据用户id获取菜单
    :param user_id: 用户id
    :return: 菜单列表
    """
    menus = SysMenu.objects.raw("""
        select distinct m.menu_id, m.parent_id, m.menu_name, m.path, m.component, m.`query`, m.route_name, m.visible, m.status, ifnull(m.perms,'') as perms, m.is_frame, m.is_cache, m.menu_type, m.icon, m.order_num, m.create_time
		from sys_menu m
			 left join sys_role_menu rm on m.menu_id = rm.menu_id
			 left join sys_user_role ur on rm.role_id = ur.role_id
			 left join sys_role ro on ur.role_id = ro.role_id
			 left join sys_user u on ur.user_id = u.user_id
		where u.user_id = %s and m.menu_type in ('M', 'C') and m.status = 0  AND ro.status = 0
		order by m.parent_id, m.order_num
    """, [user_id])

    if menus and len(menus) > 0:
        menus_data = []
        for menu in menus:
            menus_data.append(SysMenuSerializer(menu).data)
        return menus_data

    return []




def __get_memu_permission_by_role_name(role_name: str) -> tuple:
    menus = SysMenu.objects.raw("""
        select distinct m.menu_id, m.perms
		from sys_menu m
			 left join sys_role_menu rm on m.menu_id = rm.menu_id
			 left join sys_role sr on sr.role_id = rm.role_id
		where m.status = '0' and sr.role_name = %s
    """, [role_name])
    if menus and len(menus) > 0:
        list_data = []
        for val in menus:
            if val.perms:
                arr_data = val.perms.strip().split(",")
                list_data.extend([v for v in arr_data])
        return tuple(list_data)

    return tuple()



def __get_memu_permission_by_user_id(user_id: int) -> tuple:
    menus = SysMenu.objects.raw("""
        select distinct m.menu_id, m.perms
		from sys_menu m
			 left join sys_role_menu rm on m.menu_id = rm.menu_id
			 left join sys_user_role ur on rm.role_id = ur.role_id
			 left join sys_role r on r.role_id = ur.role_id
		where m.status = '0' and r.status = '0' and ur.user_id = %s
    """, [user_id])
    if menus and len(menus) > 0:
        list_data = []
        for val in menus:
            if val.perms:
                arr_data = val.perms.strip().split(",")
                list_data.extend([v for v in arr_data])
        return tuple(list_data)

    return tuple()



def __get_role_permission(user_id: int):
    return SysRole.objects.raw("""
        select distinct r.role_id, r.role_name, r.role_key, r.role_sort, r.data_scope, r.menu_check_strictly, r.dept_check_strictly,
            r.status, r.del_flag, r.create_time, r.remark 
        from sys_role r
	        left join sys_user_role ur on ur.role_id = r.role_id
	        left join sys_user u on u.user_id = ur.user_id
	        left join sys_dept d on u.dept_id = d.dept_id
	    WHERE r.del_flag = '0' and ur.user_id = %s
    """, [user_id])
