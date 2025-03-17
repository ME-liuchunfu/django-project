from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, ParseRequestMetaUser, RequestBody, RequestPostParams
from system.dict.type.services import DictTypeService


class DictTypeListView(View):

    """
    字典类型管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = DictTypeService().dict_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = DictTypeService().export_dict(req_data=req_data)
        return response


class DictTypeInfoView(View):
    """
    字典类型信息
    """

    def get(self, request, dict_ids):
        res_data = DictTypeService().dict_info(dict_id=int(dict_ids))
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, dict_ids):
        dict_ids = [ int(v) for v in dict_ids.split(',')]
        res_data = DictTypeService().del_dict(dict_ids=dict_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = DictTypeService().add_dict(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data, _msg = DictTypeService().update_dict(user_id=user_id, user_name=user_name, dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500, msg=_msg)