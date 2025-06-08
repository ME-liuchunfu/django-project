from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams
from components.log_back_decorator import log_async_logger, BusinessType
from components.request_decorator import has_permis
from generator.gen.services import GenService


class GenViewList(View):

    @has_permis("tool:gen:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = GenService().list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    @log_async_logger(title="代码生成", business_type=BusinessType.IMPORT)
    @has_permis("tool:gen:import")
    def post(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = GenService().import_list(req_data)
        return AjaxJsonResponse(extra_dict=res_data)


class GenDbList(View):

    @has_permis("tool:gen:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = GenService().db_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)