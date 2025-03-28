from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, ParseRequestMetaUser, RequestBody, RequestPostParams
from monitor.operlog.services import OperLogService


class OperLogListView(View):

    """
    通知公告管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = OperLogService().oper_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = OperLogService().export_oper(req_data=req_data)
        return response

    def delete(self, request):
        res_datas = OperLogService().clean_list()
        return AjaxJsonResponse(data=res_datas)

class OperLogInfoView(View):
    """
    通知公告信息
    """

    def get(self, request, oper_ids):
        res_data = OperLogService().oper_info(oper_id=int(oper_ids))
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, oper_ids):
        oper_ids = [ int(v) for v in oper_ids.split(',')]
        res_data = OperLogService().del_oper(oper_ids=oper_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = OperLogService().add_oper(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = OperLogService().update_oper(user_id=user_id, user_name=user_name, oper=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)