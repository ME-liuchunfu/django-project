import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysConfig
from system.serializers.models import SysConfigSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class ConfigService:

    def search_key_handler(self, k):
        if k == 'config_name' or k == 'config_key':
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def config_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            parse_page_result = ParsePageResult()
            query_set = SysConfig.objects.filter(**sql_params_dict).order_by("config_id").all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询参数设置列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysConfig) -> Any | None:
        try:
            return keys_to_camel(SysConfigSerializer(data).data)
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def config_info(self, config_id: int) -> dict:
        res_data = {}
        try:
            data = SysConfig.objects.filter(config_id=config_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询参数设置信息]异常, config_id: {config_id}', exc_info=True)
        return res_data

    def del_config(self, config_ids: list[int]) -> int:
        try:
            row, _ = SysConfig.objects.filter(config_id__in=config_ids).delete()
            return row
        except Exception as e:
            logger.error(f'[删除参数设置信息]异常, config_ids: {config_ids}', exc_info=True)
            return 0

    def add_config(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()
            # 判断 role_key 是否存在
            cache_config_key = SysConfig.objects.filter(config_key=add_dict['config_key']).all()
            if cache_config_key and len(cache_config_key) > 0:
                return -1, '参数配置已存在'

            all_columns = get_model_fields_name(SysConfig)
            del_not_model_key(add_dict, all_columns)
            sys_config = SysConfig(**add_dict)
            sys_config.save()
            return 1, None
        except Exception as e:
            logger.error(f'[新增参数设置信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_config(self, user_id: int, user_name: str, config: dict) -> tuple:
        try:
            config = keys_to_snake(config)
            update_dict = {}
            if not config.get('config_id'):
                return -1, "参数错误"

            all_columns = get_model_fields_name(SysConfig)
            read_only_keys = ['create_by', 'create_time', 'config_id', 'update_time']
            for key, value in config.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            cache_config_key = SysConfig.objects.filter(config_key=update_dict['config_key']).all()
            if (cache_config_key and len(cache_config_key) > 0
                    and cache_config_key[0].config_id != config['config_id']):
                return -1, '参数配置已存在'
            all_columns = get_model_fields_name(SysConfig)
            del_not_model_key(update_dict, all_columns)
            row = SysConfig.objects.filter(config_id=config.get('config_id')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新参数设置异常],req_dict:{config}', exc_info=True)
            return -1, '更新参数设置异常'

        return row, None

    def export_config(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            query_set = SysConfig.objects.filter(**sql_params_dict).order_by("config_id").all()
            response = ResponseStream().query_set_to_excel_http_response(name="参数设置信息", query_set=query_set)
            return response
        except Exception as e:
            logger.error(f'[导出参数设置信息]异常')
            raise ValueError('导出参数设置信息异常') from e

    def values_config_key(self, config_key: str) -> str:
        res_data = ""
        try:
            if config_key:
                query_set = SysConfig.objects.filter(config_key=config_key).all()
                if query_set and len(query_set) > 0:
                    res_data = query_set[0].config_value
        except Exception as e:
            logger.error(f'[查询参数设置信息值]异常,config_key:{config_key}', exc_info=True)

        if res_data is None:
            res_data = ""
        return res_data
