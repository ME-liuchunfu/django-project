from django.views import View
from common.http import AjaxJsonResponse, ParseRequestMetaUser, RequestGetParams, RequestPostParams, RequestBody
from system.dept.services import DeptService
from system.user.dto_serializers import UserInfoDto
from system.user.permission_services import get_role_permission, get_menu_permission
from system.user.services import UserService


class UserListView(View):

    """
    通知公告管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = UserService().user_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = UserService().export_user(req_data=req_data)
        return response

    def delete(self, request):
        res_datas = UserService().clean_list()
        return AjaxJsonResponse(data=res_datas)


class UserInfoView(View):
    """
    通知公告信息
    """

    def get(self, request, user_ids):
        res_data = UserService().user_info(user_id=int(user_ids))
        return AjaxJsonResponse(extra_dict=res_data)

    def delete(self, request, user_ids):
        user_ids = [ int(v) for v in user_ids.split(',')]
        res_data = UserService().del_user(user_ids=user_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = UserService().add_user(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = UserService().update_user(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)




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


class UserDeptTreeView(View):

    def get(self, request):
        dept_service = DeptService()
        res_datas = dept_service.dept_tree_list(params_dict={})
        res_datas = dept_service.build_dept_tree(res_datas)
        return AjaxJsonResponse(data=res_datas)


class UserInfoGetView(View):

    def get(self, request):
        res_data = UserService().user_info()
        return AjaxJsonResponse(extra_dict=res_data)