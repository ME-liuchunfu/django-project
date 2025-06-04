from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, RequestBody, RequestPostParams
from components import request_decorator
from components.log_back_decorator import log_async_logger, BusinessType
from components.request_decorator import has_permis
from system.dict.data.services import DictDataService


class DictDataListView(View):

    """
    字典值管理
    """

    @has_permis("system:dict:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = DictDataService().dict_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    @log_async_logger(title="字典类型管理", business_type=BusinessType.EXPORT)
    @has_permis("system:dict:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = DictDataService().export_dict(req_data=req_data)
        return response


class DictDataInfoView(View):
    """
    字典值信息
    """

    @has_permis("system:dict:query")
    def get(self, request, dict_ids):
        res_data = DictDataService().dict_info(dict_code=int(dict_ids))
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="字典类型管理", business_type=BusinessType.DELETE)
    @has_permis("system:dict:remove")
    def delete(self, request, dict_ids):
        dict_codes = [ int(v) for v in dict_ids.split(',')]
        res_data = DictDataService().del_dict(dict_codes=dict_codes)
        return AjaxJsonResponse(data=res_data)

    @log_async_logger(title="字典类型管理", business_type=BusinessType.INSERT)
    @has_permis("system:dict:add")
    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data, _msg = DictDataService().add_dict(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    @log_async_logger(title="字典类型管理", business_type=BusinessType.UPDATE)
    @has_permis("system:dict:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = DictDataService().update_dict(user_id=request_decorator.user_id(), user_name=request_decorator.username(), dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)