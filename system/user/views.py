from django.views import View
from common.http import AjaxJsonResponse, ParseRequestMetaUser


class LoginUserInfoView(View):
    """
    用户信息
    """

    def get(self, request):
        """
        需要返回用户信息和权限角色信息
        :param request:
        :return:
        """
        auto_user = ParseRequestMetaUser(request)()
        return AjaxJsonResponse(msg='success', extra_dict=auto_user)