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

    def __str__(self):
        return self.data.__str__()


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
            self.data['name'] = get_route_name(data)
            self.data['path'] = get_route_name(data)
            self.data['hidden'] = data.get('visible')
            self.data['component'] = get_component(data)
            self.data['query'] = data.get('query')
            link = data.get('path') if is_http(data.get('path')) else None
            self.set_meta(MetaVo(
                {
                'title': data.get('menu_name'),
                'icon': data.get('icon'),
                'noCache': data.get('is_cache') == '1',
                'link': link
                }
            ))
            if 'visible' in data and not isinstance(data.get('visible'), bool):
                self.data['hidden'] = data.get('visible') == '1'

    def data_value(self, key, value):
        self.data[key] = value


    def set_meta(self, meta: MetaVo = None):
        self.data['meta'] = meta

    def __str__(self):
        return self.data.__str__()


def get_routers(user_id:int) -> list:
    if ADMIN_USER_ID == user_id:
        menus_list = __get_menu_tree_all()
    else:
        menus_list = __get_menu_tree_by_user_id(user_id)

    menus_list = get_child_perms(menus_list, 0)
    tree_datas = build_tree_menus(menus_list)
    return tree_datas


def get_child_perms(menus_list: list, parent_id: int) -> list:
    ret_data_list = []
    for menu in menus_list:
        if menu.get('parent_id') == parent_id:
            recursion_fn(menus_list, menu)
            ret_data_list.append(menu)

    return ret_data_list


def recursion_fn(menus_list: list, menu):
    # 得到子节点列表
    child_list = get_child_list(menus_list, menu)
    menu['children'] = child_list
    for child in child_list:
        if has_child(menus_list, child):
            recursion_fn(menus_list, child)


def get_child_list(menus_list: list, menu) -> list:
    ret_list = []
    for menus in menus_list:
        if menus.get('parent_id') == menu.get('menu_id'):
            ret_list.append(menus)

    return ret_list


def has_child(menus_list: list, menu) -> bool:
    return len(get_child_list(menus_list, menu)) > 0


def build_tree_menus(menus_list: list) -> list:
    tree_datas = []
    for menu in menus_list:
        router_vo = RouterVo(menu)
        children = menu.get('children')
        if children and len(children) > 0 and "M" == menu.get('menu_type'):
            router_vo.data_value('redirect', 'noRedirect')
            router_vo.data_value('alwaysShow', True)
            router_vo.data_value('children', build_tree_menus(children))
        elif is_menu_frame(menu):
            router_vo.set_meta(None)
            children_list = []
            router = RouterVo()
            router.data_value('path', menu.get('path'))
            router.data_value('component', menu.get('component'))
            router.data_value('name', get_route_name(menu))
            router.set_meta(MetaVo({
                'title': menu.get('menu_name'),
                'icon': menu.get('icon'),
                'noCache': "1" == menu.get('is_cache'),
                'link': menu.get('path')
            }))
            children_list.append(router)
            router_vo.data_value('children', children_list)

        elif menu.get('parent_id') == 0 and is_inner_link(menu):
            router_vo.set_meta(MetaVo({'title': menu.get('menu_name'), 'icon': menu.get('icon')}))
            router_vo.data_value('path', '/')
            children_list = []
            router = RouterVo()
            router_path = inner_link_replace_each(menu.get('path'))
            router.data_value('path', router_path)
            router.data_value('component', "InnerLink")
            router.data_value('name', get_route_name(menu))
            router.set_meta(MetaVo({
                'title': menu.get('menu_name'),
                'icon': menu.get('icon'),
                'link': menu.get('path')
            }))
            children_list.append(router)
            router_vo.data_value('children', children_list)

        tree_datas.append(router_vo)


    return tree_datas


class Constants:
    HTTP = "http://"
    HTTPS = "https://"
    WWW = "www."
    DOT = "."
    COLON = ":"


def inner_link_replace_each(path):
    """
    Replace specific substrings in the given URL path.

    :param path: The URL path to be modified
    :return: Modified URL path
    """
    path = path.replace(Constants.HTTP, "")
    path = path.replace(Constants.HTTPS, "")
    path = path.replace(Constants.WWW, "")
    path = path.replace(Constants.DOT, "/")
    path = path.replace(Constants.COLON, "/")
    return path

def get_component(menu: dict):
    component = "Layout"
    if menu.get('component') and not is_menu_frame(menu):
        component = menu.get('component')
    elif not menu.get('component') and menu.get('parent_id') != 0 and is_inner_link(menu):
        component = "InnerLink"
    elif not menu.get('component') and is_parent_view(menu):
        component = "ParentView"
    return component


def is_parent_view(menu: dict) -> bool:
    return menu.get('parent_id') != 0 and "M" == menu.get('menu_type')


def is_inner_link(menu: dict) -> bool:
    return menu.get('is_frame') == "1" and is_http(menu.get('path'))


def is_http(val: str) -> bool:
    if not val:
        return False
    return val.startswith('http:') or val.startswith('https:')


def is_menu_frame(menu: dict) -> bool:
    return menu.get('parent_id') == 0 and "C" == menu.get('menu_type') and menu.get('is_frame') == "1"


def get_route_name(menu: dict):
    """
    Get the route name from the menu information.

    :param menu: SysMenu object containing menu information
    :return: The route name
    """
    if menu.get('is_frame'):
        return ""
    return format_route_name(menu.get('route_name'), menu.get('path'))


def format_route_name(name, path):
    """
    Get the route name, or use the route path if the route name is not set.

    :param name: The route name
    :param path: The route path
    :return: The route name in capitalized format
    """
    router_name = name if name else path
    return router_name.capitalize()


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
