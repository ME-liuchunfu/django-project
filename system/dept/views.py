from django.views import View

from common.http import RequestGetParams, AjaxJsonResponse, RequestPostParams, RequestBody
from components import request_decorator
from components.request_decorator import has_permis
from system.dept.services import DeptService


class DeptListView(View):

    """
    部门管理
    """

    @has_permis("system:dept:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = DeptService().dept_list(req_data)
        return AjaxJsonResponse(data=res_data)

    @has_permis("system:dept:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = DeptService().export_dept(req_data)
        return response


class DeptInfoView(View):
    """
    部门信息
    """

    @has_permis("system:dept:query")
    def get(self, request, post_id):
        res_data = DeptService().dept_info(post_id)
        return AjaxJsonResponse(data=res_data)

    @has_permis("system:dept:remove")
    def delete(self, request, post_id):
        res_data = DeptService().del_dept(post_id)
        return AjaxJsonResponse(data=res_data)

    @has_permis("system:dept:add")
    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data = DeptService().add_dept(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)

    @has_permis("system:dept:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data = DeptService().update_dept(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)


class DeptExcludeView(View):

    @has_permis("system:dept:query")
    def get(self, request, dept_id: int):
        res_data = DeptService().exclude_dept_list(dept_id=dept_id, req_dict={})
        return AjaxJsonResponse(data=res_data)