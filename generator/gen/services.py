import logging
import re
from typing import Optional, Any

from django.db.models import Q

from common.data_frame import PageResult, ParsePageResult, inject_sql_params_dict, parse_sql_columns, \
    remove_order_columns, inject_page_params
from common.utils import keys_to_snake, keys_to_camel
from components.request_decorator import username
from generator.models import GenTable, VerTableInfo
from generator.serializers.models import GenTableSerializer, VerTableInfoSerializer

logger = logging.getLogger(__name__)


class GenService:

    def search_key_handler(self, k):
        if k in ['table_name', 'table_comment']:
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def import_list(self, req_dict: dict) -> dict:
        rest = {}
        try:
            # 查询表名
            tables_str = req_dict.get('tables', None)
            if tables_str is None:
                return rest
            tables = f"{tables_str}".split(",")
            query_set = (VerTableInfo.objects.using('information_schema')
                         .filter(~Q(table_name__startswith='qrtz_') & ~Q(table_name__startswith='gen_'))
                         .filter(table_name__in=tables))

            user_name = username()
            for query in query_set:
                gen_table: GenTable = self.__init_table(query, user_name)
                gen_table.save()
                if gen_table.table_id is not None:
                    # 保存列信息
                    pass
        except Exception as e:
            logger.error(f'[导入gen数据表错误],req_dict:{req_dict}', exc_info=True)
        return rest


    def __init_table(self, query: str, user_name: str) -> GenTable:
        pass
    def list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            order_dict = remove_order_columns(sql_params_dict)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            parse_page_result = ParsePageResult()
            exec = GenTable.objects.filter(**sql_params_dict)
            if order_dict.get('is_asc') is not None and order_dict.get('order_column') is not None:
                if order_dict.get('is_asc') is True:
                    exec.order_by(order_dict.get('order_column'))
                else:
                    exec.order_by(f"-{order_dict.get('order_column')}")

            query_set = exec.all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询gen列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def db_list(self, req_data: dict) -> PageResult:
        try:
            tableName = req_data.get('tableName', None)
            tableComment = req_data.get('tableComment', None)
            params_beginTime = req_data.get('params.beginTime', None)
            params_endTime = req_data.get('params.endTime', None)

            parse_page_result = ParsePageResult()
            query_set = VerTableInfo.objects.using('information_schema').filter(~Q(table_name__startswith='qrtz_')
                                                    & ~Q(table_name__startswith='gen_')).order_by("-create_time")
            if tableName is not None and tableName != '':
                query_set.filter(table_name__icontains=tableName)

            if tableComment is not None and tableComment != '':
                query_set.filter(table_comment__icontains=tableComment)

            if params_beginTime is not None and params_beginTime != '':
                query_set.filter(create_time__gt=params_beginTime)

            if params_endTime is not None and params_endTime != '':
                query_set.filter(create_time__lte=params_endTime)

            query_set.all()
            parse_page_result.set_convert_handler(self.serializer_table_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询gen列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: GenTable) -> Optional[Any]:
        try:
            res = keys_to_camel(GenTableSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def serializer_table_model(self, data: VerTableInfo) -> Optional[Any]:
        try:
            res = keys_to_camel(VerTableInfoSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None