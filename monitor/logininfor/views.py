from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, RequestBody, RequestPostParams
from components import request_decorator
from monitor.logininfor.services import LogininforService


class LogininforListView(View):

    """
    通知公告管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = LogininforService().info_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = LogininforService().export_info(req_data=req_data)
        return response

    def delete(self, request):
        res_datas = LogininforService().clean_list()
        return AjaxJsonResponse(data=res_datas)


class LogininforInfoView(View):
    """
    通知公告信息
    """

    def get(self, request, info_ids):
        res_data = LogininforService().info_info(info_id=int(info_ids))
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, info_ids):
        info_ids = [ int(v) for v in info_ids.split(',')]
        res_data = LogininforService().del_info(info_ids=info_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data, _msg = LogininforService().add_info(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = LogininforService().update_info(user_id=request_decorator.user_id(), user_name=request_decorator.username(), info=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)