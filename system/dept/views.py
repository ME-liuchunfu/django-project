from django.views import View

from common.http import RequestGetParams, AjaxJsonResponse, RequestPostParams, ParseRequestMetaUser, RequestBody
from system.dept.services import DeptService


class DeptListView(View):

    """
    部门管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = DeptService().dept_list(req_data)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = DeptService().export_dept(req_data)
        return response


class DeptInfoView(View):
    """
    部门信息
    """

    def get(self, request, post_id):
        res_data = DeptService().dept_info(post_id)
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, post_id):
        res_data = DeptService().del_dept(post_id)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data = DeptService().add_dept(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data = DeptService().update_dept(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)


class DeptExcludeView(View):

    def get(self, request, dept_id: int):
        res_data = DeptService().exclude_dept_list(dept_id=dept_id, req_dict={})
        return AjaxJsonResponse(data=res_data)