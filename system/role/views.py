from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, RequestBody, RequestPostParams
from components import request_decorator
from components.log_back_decorator import log_async_logger, BusinessType
from components.request_decorator import has_permis
from system.role.services import RoleService


class RoleListView(View):

    """
    角色管理
    """

    @has_permis("system:role:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = RoleService().role_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    @log_async_logger(title="角色管理", business_type=BusinessType.EXPORT)
    @has_permis("system:role:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = RoleService().export_role(req_data)
        return response


class RoleInfoView(View):
    """
    角色信息
    """

    @has_permis("system:role:query")
    def get(self, request, role_ids):
        res_data = RoleService().role_info(role_id=int(role_ids))
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="岗位管理", business_type=BusinessType.DELETE)
    @has_permis("system:role:remove")
    def delete(self, request, role_ids):
        role_ids = [int(v) for v in role_ids.split(',')]
        res_data = RoleService().del_role(role_ids=role_ids)
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="岗位管理", business_type=BusinessType.INSERT)
    @has_permis("system:role:add")
    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data, _msg = RoleService().add_role(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg= _msg if _msg else None)

    @log_async_logger(title="岗位管理", business_type=BusinessType.UPDATE)
    @has_permis("system:role:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = RoleService().update_role(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
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