import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns, sql_date_parse, del_int_column_key, sql_order_by_parse
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from monitor.models import SysOperLog
from monitor.serializers.models import SysOperLogSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class OperLogService:

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

    def oper_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            parse_page_result = ParsePageResult()
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            order_columns = sql_order_by_parse(req_data=req_data, default_vals=['oper_id'])
            query_set = SysOperLog.objects.filter(**sql_params_dict).order_by(*order_columns).all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询操作日志记录列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysOperLog) -> Any | None:
        try:
            res = keys_to_camel(SysOperLogSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def oper_info(self, oper_id: int) -> dict:
        res_data = {}
        try:
            data = SysOperLog.objects.filter(oper_id=oper_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询操作日志记录信息]异常, oper_id: {oper_id}', exc_info=True)
        return res_data

    def del_oper(self, oper_ids: list[int]) -> int:
        try:
            row, _ = SysOperLog.objects.filter(oper_id__in=oper_ids).delete()
            return row
        except Exception as e:
            logger.error(f'[删除操作日志记录信息]异常, oper_ids: {oper_ids}', exc_info=True)
            return 0

    def add_oper(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()

            all_columns = get_model_fields_name(SysOperLog)
            del_not_model_key(add_dict, all_columns)
            sys_oper = SysOperLog(**add_dict)
            sys_oper.save()
            return 1, None
        except Exception as e:
            logger.error(f'[新增操作日志记录信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_oper(self, user_id: int, user_name: str, oper: dict) -> tuple:
        try:
            oper = keys_to_snake(oper)
            update_dict = {}
            if not oper.get('oper_id'):
                return -1, "参数错误"

            all_columns = get_model_fields_name(SysOperLog)
            read_only_keys = ['create_by', 'create_time', 'oper_id', 'update_time']
            for key, value in oper.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            all_columns = get_model_fields_name(SysOperLog)
            del_not_model_key(update_dict, all_columns)
            row = SysOperLog.objects.filter(oper_id=oper.get('oper_id')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新操作日志记录异常],req_dict:{oper}', exc_info=True)
            return -1, '更新操作日志记录异常'

        return row, None

    def export_oper(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict, columns=self.get_time_columns())
            del_int_column_key(sql_params_dict, ['is_asc', 'order_by_column'])
            order_columns = sql_order_by_parse(req_data=req_data, default_vals=['oper_id'])
            query_set = SysOperLog.objects.filter(**sql_params_dict).order_by(*order_columns).all()
            response = ResponseStream().query_set_to_excel_http_response(name="操作日志记录信息", query_set=query_set, time_fields=['login_time'])
            return response
        except Exception as e:
            logger.error(f'[导出操作日志记录信息]异常')
            raise ValueError('导出操作日志记录信息异常') from e

    def clean_list(self) -> int:
        row = 0
        try:
            row, _ = SysOperLog.objects.all().delete()
        except Exception as e:
            logger.error(f'[清空操作日志]异常', exc_info=True)
        return row
