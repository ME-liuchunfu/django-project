import logging
from typing import Any
import pandas as pd
from django.http import FileResponse, HttpResponse
from django.utils import timezone

from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysPost
from system.serializers.models import SysPostSerializer

logger = logging.getLogger(__name__)


class PostService:

    def search_key_handler(self, k):
        if k == 'post_code' or k == 'post_name':
            return f'{k}__icontains'
        return k

    def post_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_page_result = ParsePageResult()
            query_set = SysPost.objects.filter(**sql_params_dict).all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询岗位列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysPost) -> Any | None:
        try:
            return keys_to_camel(SysPostSerializer(data).data)
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def post_info(self, post_id: int) -> dict:
        res_data = {}
        try:
            data = SysPost.objects.filter(post_id=post_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询岗位信息]异常, post_id: {post_id}', exc_info=True)
        return res_data

    def del_post(self, post_id: int) -> int:
        try:
            row, _ = SysPost.objects.filter(post_id=post_id).delete()
            return row
        except Exception as e:
            logger.error(f'[删除岗位信息]异常, post_id: {post_id}', exc_info=True)
            return 0

    def add_post(self, user_id: int, user_name: str, req_dict: dict) -> int:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()
            sys_post = SysPost(**add_dict)
            sys_post.save()
            return 1
        except Exception as e:
            logger.error(f'[新增岗位信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}', exc_info=True)
            return 0

    def update_post(self, user_id: int, user_name: str, post: dict) -> int:
        try:
            post = keys_to_snake(post)
            update_dict = {}
            if not post.get('post_id'):
                raise ValueError("参数错误")

            read_only_keys = ['create_by', 'create_time', 'post_id', 'update_time']
            for key, value in post.items():
                if key in read_only_keys:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            row = SysPost.objects.filter(post_id=post.get('post_id')).update(**update_dict)
        except Exception as e:
            row = 0
            logger.error(f'[更新岗位异常],req_dict:{post}', exc_info=True)

        return row

    def export_post(self, req_data : dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            query_set = SysPost.objects.filter(**sql_params_dict).all()
            res_datas = list(query_set.values())
            df = pd.DataFrame(res_datas)
            response_stream = ResponseStream()
            response = response_stream.excel_http_response(name="岗位信息")
            if 'create_time' in df.columns:
                # 将带时区的日期时间转换为无时区的日期时间
                df['create_time'] = df['create_time'].dt.tz_localize(None)

            if 'update_time' in df.columns:
                # 将带时区的日期时间转换为无时区的日期时间
                df['update_time'] = df['update_time'].dt.tz_localize(None)

            df.to_excel(response, index=False, engine='openpyxl')
            return response
        except Exception as e:
            logger.error(f'[导出岗位信息]异常')
            raise ValueError('导出岗位信息异常') from e
