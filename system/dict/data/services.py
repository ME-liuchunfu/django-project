import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysDictData
from system.serializers.models import SysDictDataSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class DictDataService:

    def search_key_handler(self, k):
        if k == 'dict_label':
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def dict_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            parse_page_result = ParsePageResult()
            query_set = SysDictData.objects.filter(**sql_params_dict).order_by("dict_code").all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询字典值列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysDictData) -> Any | None:
        try:
            res = keys_to_camel(SysDictDataSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def dict_info(self, dict_code: int) -> dict:
        res_data = {}
        try:
            data = SysDictData.objects.filter(dict_code=dict_code).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询字典值信息]异常, dict_code: {dict_code}', exc_info=True)
        return res_data

    def del_dict(self, dict_codes: list[int]) -> int:
        try:
            row, _ = SysDictData.objects.filter(dict_code__in=dict_codes).delete()
            return row
        except Exception as e:
            logger.error(f'[删除字典值信息]异常, dict_codes: {dict_codes}', exc_info=True)
            return 0

    def add_dict(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()

            all_columns = get_model_fields_name(SysDictData)
            del_not_model_key(add_dict, all_columns)
            sys_dict = SysDictData(**add_dict)
            sys_dict.save()
            return 1, None
        except Exception as e:
            logger.error(f'[新增字典值信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_dict(self, user_id: int, user_name: str, dict: dict) -> tuple:
        try:
            dict = keys_to_snake(dict)
            update_dict = {}
            if not dict.get('dict_code'):
                return -1, "参数错误"

            all_columns = get_model_fields_name(SysDictData)
            read_only_keys = ['create_by', 'create_time', 'dict_code', 'update_time']
            for key, value in dict.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            all_columns = get_model_fields_name(SysDictData)
            del_not_model_key(update_dict, all_columns)
            row = SysDictData.objects.filter(dict_code=dict.get('dict_code')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新字典值异常],req_dict:{dict}', exc_info=True)
            return -1, '更新字典值异常'

        return row, None

    def export_dict(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            query_set = SysDictData.objects.filter(**sql_params_dict).order_by("dict_code").all()
            response = ResponseStream().query_set_to_excel_http_response(name="字典值信息", query_set=query_set)
            return response
        except Exception as e:
            logger.error(f'[导出字典值信息]异常')
            raise ValueError('导出字典值信息异常') from e
