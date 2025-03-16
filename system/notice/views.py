from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, ParseRequestMetaUser, RequestBody, RequestPostParams
from system.notice.services import NoticeService


class NoticeListView(View):

    """
    通知公告管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = NoticeService().notice_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = NoticeService().export_notice(req_data=req_data)
        return response


class NoticeInfoView(View):
    """
    通知公告信息
    """

    def get(self, request, notice_ids):
        res_data = NoticeService().notice_info(notice_id=int(notice_ids))
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, notice_ids):
        notice_ids = [ int(v) for v in notice_ids.split(',')]
        res_data = NoticeService().del_notice(notice_ids=notice_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = NoticeService().add_notice(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = NoticeService().update_notice(user_id=user_id, user_name=user_name, notice=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)