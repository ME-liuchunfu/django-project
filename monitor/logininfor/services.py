import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns, sql_date_parse, del_int_column_key
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysLogininfor
from system.serializers.models import SysLogininforSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class LogininforService:

    def search_key_handler(self, k):
        if k in ['title', 'oper_ip', 'oper_name']:
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def get_time_columns(self):
        return {
            'login_time': {
                "convert": sql_date_parse,
                "format": "%Y-%m-%d %H:%M:%S",
                "val": ['params[begin_time]', 'params[end_time]']
            },
        }

    def info_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            parse_page_result = ParsePageResult()
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            query_set = SysLogininfor.objects.filter(**sql_params_dict).order_by("info_id").all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询登录日志记录列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysLogininfor) -> Any | None:
        try:
            res = keys_to_camel(SysLogininforSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def info_info(self, info_id: int) -> dict:
        res_data = {}
        try:
            data = SysLogininfor.objects.filter(info_id=info_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询登录日志记录信息]异常, info_id: {info_id}', exc_info=True)
        return res_data

    def del_info(self, info_ids: list[int]) -> int:
        try:
            row, _ = SysLogininfor.objects.filter(info_id__in=info_ids).delete()
            return row
        except Exception as e:
            logger.error(f'[删除登录日志记录信息]异常, info_ids: {info_ids}', exc_info=True)
            return 0

    def add_info(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()

            all_columns = get_model_fields_name(SysLogininfor)
            del_not_model_key(add_dict, all_columns)
            sys_info = SysLogininfor(**add_dict)
            sys_info.save()
            return 1, None
        except Exception as e:
            logger.error(f'[新增登录日志记录信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_info(self, user_id: int, user_name: str, info: dict) -> tuple:
        try:
            info = keys_to_snake(info)
            update_dict = {}
            if not info.get('info_id'):
                return -1, "参数错误"

            all_columns = get_model_fields_name(SysLogininfor)
            read_only_keys = ['create_by', 'create_time', 'info_id', 'update_time']
            for key, value in info.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            all_columns = get_model_fields_name(SysLogininfor)
            del_not_model_key(update_dict, all_columns)
            row = SysLogininfor.objects.filter(info_id=info.get('info_id')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新登录日志记录异常],req_dict:{info}', exc_info=True)
            return -1, '更新登录日志记录异常'

        return row, None

    def export_info(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            query_set = SysLogininfor.objects.filter(**sql_params_dict).order_by("info_id").all()
            response = ResponseStream().query_set_to_excel_http_response(name="登录日志记录信息", query_set=query_set, time_fields=['login_time'])
            return response
        except Exception as e:
            logger.error(f'[导出登录日志记录信息]异常')
            raise ValueError('导出登录日志记录信息异常') from e

    def clean_list(self) -> int:
        row = 0
        try:
            row, _ = SysLogininfor.objects.all().delete()
        except Exception as e:
            logger.error(f'[清空登录日志]异常')
        return row
