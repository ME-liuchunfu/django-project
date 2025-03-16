import logging

from system.models import SysRoleMenu

logger = logging.getLogger(__name__)

class RoleMenuService:

    def batch_role_menu(self, role_menus: list[SysRoleMenu] = None) -> int:
        if not role_menus or len(role_menus) == 0:
            return 0
        else:
            rest = SysRoleMenu.objects.bulk_create(role_menus)
            return len(rest)

    def del_role_menus(self, role_id: int):
       try:
           SysRoleMenu.objects.filter(role_id=role_id).delete()
       except Exception as e:
           logger.error(f'[删除角色菜单失败], role_id:{role_id}')