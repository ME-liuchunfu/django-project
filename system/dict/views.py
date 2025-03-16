from django.views import View

from common.http import AjaxJsonResponse
from system.dict.services import DictDataService


class DictDataType(View):

    """
    获取字典值
    """

    def get(self, request, dict_type):
        ret_datas = DictDataService().get_dict_datas_by_type(dict_type=dict_type)
        return AjaxJsonResponse(data=ret_datas)