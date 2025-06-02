from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, RequestBody, RequestPostParams
from components import request_decorator
from components.request_decorator import has_permis
from system.config.services import ConfigService


class ConfigListView(View):

    """
    参数设置管理
    """

    @has_permis("system:config:list")
    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = ConfigService().config_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    @has_permis("system:config:export")
    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = ConfigService().export_config(req_data=req_data)
        return response

    @has_permis("system:config:delete")
    def delete(self, request):
        # todo test
        return AjaxJsonResponse()


class ConfigInfoView(View):
    """
    参数设置信息
    """

    @has_permis("system:config:query")
    def get(self, request, config_ids):
        res_data = ConfigService().config_info(config_id=int(config_ids))
        return AjaxJsonResponse(data=res_data)

    @has_permis("system:config:remove")
    def delete(self, request, config_ids):
        config_ids = [ int(v) for v in config_ids.split(',')]
        res_data = ConfigService().del_config(config_ids=config_ids)
        return AjaxJsonResponse(data=res_data)

    @has_permis("system:config:add")
    def post(self, request):
        req_dict= RequestBody(request).get_data()
        res_data, _msg = ConfigService().add_config(user_id=request_decorator.user_id(), user_name=request_decorator.username(), req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    @has_permis("system:config:edit")
    def put(self, request):
        req_dict = RequestBody(request).get_data()
        res_data, _msg = ConfigService().update_config(user_id=request_decorator.user_id(), user_name=request_decorator.username(), config=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)


class ConfigKeyView(View):

    @has_permis("system:config:query")
    def get(self, request, config_key: str):
        res_data = ConfigService().values_config_key(config_key=config_key)
        return AjaxJsonResponse(data=res_data)