from django.views import View
from common.http import AjaxJsonResponse, RequestGetParams, RequestPostParams, RequestBody
from components import request_decorator
from components.log_back_decorator import log_async_logger, BusinessType
from components.request_decorator import has_permis
from system.dept.services import DeptService
from system.user.dto_serializers import UserInfoDto
from system.user.permission_services import get_role_permission, get_menu_permission
from system.user.services import UserService


class UserListView(View):
    """
    通知公告管理
    """

    @has_permis("system:user:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = UserService().user_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)


    @log_async_logger(title="用户管理", business_type=BusinessType.EXPORT)
    @has_permis("system:user:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = UserService().export_user(req_data=req_data)
        return response

    @log_async_logger(title="用户管理", business_type=BusinessType.CLEAN)
    @has_permis("system:user:remove")
    def delete(self, request):
        res_datas = UserService().clean_list()
        return AjaxJsonResponse(data=res_datas)


class UserInfoView(View):
    """
    通知公告信息
    """

    @has_permis("system:user:query")
    def get(self, request, user_ids):
        res_data = UserService().user_info(user_id=int(user_ids))
        return AjaxJsonResponse(extra_dict=res_data)

    @log_async_logger(title="用户管理", business_type=BusinessType.DELETE)
    @has_permis("system:user:remove")
    def delete(self, request, user_ids):
        user_ids = [int(v) for v in user_ids.split(',')]
        res_data = UserService().del_user(user_ids=user_ids)
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="用户管理", business_type=BusinessType.INSERT)
    @has_permis("system:user:add")
    def post(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = UserService().add_user(user_id=request_decorator.user_id(),
                                                user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    @log_async_logger(title="用户管理", business_type=BusinessType.UPDATE)
    @has_permis("system:user:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = UserService().update_user(user_id=request_decorator.user_id(),
                                                   user_name=request_decorator.username(), req_dict=req_dict)
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
        user_id = request_decorator.user_id()
        username = request_decorator.username()
        roles = get_role_permission(user_id=user_id, username=username)
        permissions = get_menu_permission(user_id=user_id, username=username, roles=roles)
        user_info = UserInfoDto(user=request_decorator.user_data(), roles=roles, permissions=permissions).get_data()
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
