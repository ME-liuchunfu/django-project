from common.utils import keys_to_camel
from system.models import SysDictData, SysDictType
from system.serializers.models import SysDictDataSerializer, SysDictTypeSerializer


class DictDataService:

    """
    字典获取
    """

    def get_dict_datas_by_type(self, dict_type) -> list[dict]:
        data_results = SysDictData.objects.filter(status='0', dict_type=dict_type).order_by('dict_code').all()

        ret_datas = []
        if data_results and len(data_results) > 0:
            for data in data_results:
                ret_datas.append(SysDictDataSerializer(data).data)

        ret_datas = keys_to_camel(ret_datas)
        return ret_datas

    def get_dict_types(self, dict_type=None) -> list[dict]:
        sql_params = {}
        if dict_type is not None:
            sql_params['dict_type'] = dict_type
        data_results = SysDictType.objects.filter(status='0', **sql_params).all()

        ret_datas = []
        if data_results and len(data_results) > 0:
            for data in data_results:
                ret_datas.append(SysDictTypeSerializer(data).data)

        ret_datas = keys_to_camel(ret_datas)
        return ret_datas