import logging
import re
from typing import Any
from django.http import HttpResponse
from django.utils import timezone
from common.data_frame import PageResult, ParsePageResult, inject_page_params, inject_sql_params_dict, \
    get_model_fields_name, del_not_model_key, parse_sql_columns
from common.http import ResponseStream
from common.utils import keys_to_snake, keys_to_camel
from system.models import SysNotice
from system.serializers.models import SysNoticeSerializer
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER_NAME')


class NoticeService:

    def search_key_handler(self, k):
        if k == 'notice_title':
            return f'{k}__icontains'
        pattern = r'params\[[^\]]+\]'
        if re.match(pattern, k):
            return None
        return k

    def notice_list(self, req_data: dict) -> PageResult:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            parse_page_result = ParsePageResult()
            query_set = SysNotice.objects.filter(**sql_params_dict).order_by("notice_id").all()
            parse_page_result.set_convert_handler(self.serializer_model)
            inject_page_params(req_dict=req_data, parse_page=parse_page_result)
            return parse_page_result(data_query_set=query_set)
        except Exception as e:
            logger.error(f'[查询通知公告列表异常], req_data: {req_data}', exc_info=True)
            return PageResult(code=500, msg='查询异常')

    def serializer_model(self, data: SysNotice) -> Any | None:
        try:
            notice_content = data.notice_content
            if notice_content:
                data.notice_content = notice_content.decode('utf-8')
            res = keys_to_camel(SysNoticeSerializer(data).data)
            return res
        except Exception as e:
            logger.error(f'序列化异常', exc_info=True)
            return None

    def notice_info(self, notice_id: int) -> dict:
        res_data = {}
        try:
            data = SysNotice.objects.filter(notice_id=notice_id).get()
            res_data = self.serializer_model(data)
        except Exception as e:
            logger.error(f'[查询通知公告信息]异常, notice_id: {notice_id}', exc_info=True)
        return res_data

    def del_notice(self, notice_ids: list[int]) -> int:
        try:
            row, _ = SysNotice.objects.filter(notice_id__in=notice_ids).delete()
            return row
        except Exception as e:
            logger.error(f'[删除通知公告信息]异常, notice_ids: {notice_ids}', exc_info=True)
            return 0

    def add_notice(self, user_id: int, user_name: str, req_dict: dict) -> tuple:
        try:
            add_dict = keys_to_snake(req_dict)
            add_dict['create_by'] = user_name
            add_dict['create_time'] = timezone.now()

            all_columns = get_model_fields_name(SysNotice)
            del_not_model_key(add_dict, all_columns)
            sys_notice = SysNotice(**add_dict)
            sys_notice.save()
            return 1, None
        except Exception as e:
            logger.error(f'[新增通知公告信息]异常, user_id:{user_id}, user_name:{user_name}, req_dict:{req_dict}',
                         exc_info=True)
            return 0, None

    def update_notice(self, user_id: int, user_name: str, notice: dict) -> tuple:
        try:
            notice = keys_to_snake(notice)
            update_dict = {}
            if not notice.get('notice_id'):
                return -1, "参数错误"

            all_columns = get_model_fields_name(SysNotice)
            read_only_keys = ['create_by', 'create_time', 'notice_id', 'update_time']
            for key, value in notice.items():
                if key in read_only_keys:
                    continue
                if key not in all_columns:
                    continue
                update_dict[key] = value

            update_dict['update_by'] = user_name
            update_dict['update_time'] = timezone.now()
            all_columns = get_model_fields_name(SysNotice)
            del_not_model_key(update_dict, all_columns)
            row = SysNotice.objects.filter(notice_id=notice.get('notice_id')).update(**update_dict)
        except Exception as e:
            logger.error(f'[更新通知公告异常],req_dict:{notice}', exc_info=True)
            return -1, '更新通知公告异常'

        return row, None

    def export_notice(self, req_data: dict) -> HttpResponse:
        try:
            req_data = keys_to_snake(req_data)
            sql_params_dict = {}
            inject_sql_params_dict(req_dict=req_data, sql_param_dict=sql_params_dict, handler=self.search_key_handler)
            parse_sql_columns(req_dict=req_data, sql_params_dict=sql_params_dict)
            query_set = SysNotice.objects.filter(**sql_params_dict).order_by("notice_id").all()
            response = ResponseStream().query_set_to_excel_http_response(name="通知公告信息", query_set=query_set)
            return response
        except Exception as e:
            logger.error(f'[导出通知公告信息]异常')
            raise ValueError('导出通知公告信息异常') from e
