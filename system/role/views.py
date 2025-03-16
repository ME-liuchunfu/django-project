from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, ParseRequestMetaUser, RequestBody, RequestPostParams
from system.role.services import RoleService


class RoleListView(View):

    """
    角色管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = RoleService().role_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = RoleService().export_role(req_data)
        return response


class RoleInfoView(View):
    """
    角色信息
    """

    def get(self, request, role_id):
        res_data = RoleService().role_info(role_id)
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, role_id):
        res_data = RoleService().del_role(role_id)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = RoleService().add_role(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg= _msg if _msg else None)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = RoleService().update_role(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg= _msg if _msg else None)



class RoleStatusView(View):

    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_dict = RoleService().change_status(req_dict=req_dict)
        return AjaxJsonResponse(extra_dict=res_dict)


class RoleDataView(View):

    def get(self, request, role_id: int):
        res_dict = RoleService().dept_tree(role_id=role_id)
        return AjaxJsonResponse(extra_dict=res_dict)