from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, RequestBody, RequestPostParams
from components import request_decorator
from components.log_back_decorator import log_async_logger, BusinessType
from components.request_decorator import has_permis
from system.notice.services import NoticeService


class NoticeListView(View):

    """
    通知公告管理
    """

    @has_permis("system:notice:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = NoticeService().notice_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    @log_async_logger(title="公告管理", business_type=BusinessType.EXPORT)
    @has_permis("system:notice:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = NoticeService().export_notice(req_data=req_data)
        return response


class NoticeInfoView(View):
    """
    通知公告信息
    """

    @has_permis("system:notice:query")
    def get(self, request, notice_ids):
        res_data = NoticeService().notice_info(notice_id=int(notice_ids))
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="公告管理", business_type=BusinessType.DELETE)
    @has_permis("system:notice:remove")
    def delete(self, request, notice_ids):
        notice_ids = [ int(v) for v in notice_ids.split(',')]
        res_data = NoticeService().del_notice(notice_ids=notice_ids)
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="公告管理", business_type=BusinessType.INSERT)
    @has_permis("system:notice:add")
    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data, _msg = NoticeService().add_notice(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    @log_async_logger(title="公告管理", business_type=BusinessType.UPDATE)
    @has_permis("system:notice:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = NoticeService().update_notice(user_id=request_decorator.user_id(), user_name=request_decorator.username(), notice=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)