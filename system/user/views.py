from django.views import View
from common.http import AjaxJsonResponse, ParseRequestMetaUser
from system.user.dto_serializers import UserInfoDto
from system.user.permission_services import get_role_permission, get_menu_permission


class LoginUserInfoView(View):
    """
    用户信息
    """

    def get(self, request):
        """
        需要返回用户信息和权限角色信息
        :param request:
        :return: UserInfoDto {
            user:{},
            roles: (str),
            permissions: (str)
        }
        """
        auto_user = ParseRequestMetaUser(request)()
        roles = get_role_permission(auto_user.get("user_id"), auto_user.get("username"))
        permissions = get_menu_permission(auto_user.get("user_id"), auto_user.get("username"), roles=roles)
        user_info = UserInfoDto(user=auto_user, roles=roles, permissions=permissions).get_data()
        return AjaxJsonResponse(msg='success', extra_dict=user_info)