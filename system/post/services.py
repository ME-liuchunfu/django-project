import logging
from typing import Any

from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysPost
from system.serializers.models import SysPostSerializer

logger = logging.getLogger(__name__)


class PostService:

    def post_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            def search_key_handler(k):
                if k == 'post_code' or k == 'post_name':
                    return f'{k}__icontains'
                return k

            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=search_key_handler)
            parse_page_result = ParsePageResult()
            query_set = SysPost.objects.filter(**sql_params_dict).all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询岗位列表异常], req_data: {req_data}')
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysPost) -> Any | None:
        try:
            return keys_to_camel(SysPostSerializer(data).data)
        except Exception as e:
            logger.error(f'序列化异常')
            return None
