import json
import logging
import pandas as pd
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict, HttpResponse
from django.conf import settings
from django.db import models

logger = logging.getLogger(settings.APP_LOGGER_NAME)


def get_datetime_fields(model_class):
    """获取模型中所有 DateTimeField 字段的名称"""
    return [
        field.name
        for field in model_class._meta.get_fields()
        if isinstance(field, models.DateTimeField)
    ]



class AjaxJsonResponse(JsonResponse):
    """
    django 通用json数据返回
    {
        'code': 200,
        'msg': 'msg',
        'data': data
    }
    """

    def __init__(self, code: int = 200, msg: str = 'success', data=None, extra_dict: dict = None, **kwargs):
        if msg is None:
            msg = 'success'
        content = {
            'code': code,
            'msg': msg,
        }
        if data:
            content['data'] = data
        elif isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple):
            content['data'] = data

        if extra_dict:
            content.update(extra_dict)

        kwargs.setdefault('json_dumps_params', {'ensure_ascii': False})
        super().__init__(content, **kwargs)



class RequestBody:

    def __init__(self, request):
        path = ''
        try:
            path = request.path
            self.data = {}
            req_dat = json.loads(request.body)
            self.data = req_dat
        except Exception as e:
            logger.error(f"[解析参数出错]，path:{path}")

    def __call__(self, *args, **kwargs):
        return self.get_data()

    def get_data(self) -> tuple | list | dict:
        return self.data


class ParseJson:

    def __init__(self, data):
        try:
            if not isinstance(data, str):
                data = str(data)
            self.data = {}
            req_dat = json.loads(data)
            self.data = req_dat
        except Exception as e:
            logger.error(f"[解析参数出错]，data:{data}")

    def __call__(self, *args, **kwargs):
        return self.get_data()

    def get_data(self) -> tuple | list | dict:
        return self.data


class RequestGetParams:
    """
    解析http get参数
    """

    def __init__(self, request):
        self.request = request
        self.data = {}
        self.__parse(request)

    def __parse(self, request):
        path = request.path
        try:
            get_data: QueryDict = request.GET
            if get_data:
                data = get_data.dict()
                self.data = data
        except Exception as e:
            logger.error(f'[解析http get参数异常], path:{path}')

    def get_data(self) -> tuple | list | dict:
        return self.data


class RequestPostParams:
    """
    解析http post from请求参数
    """

    def __init__(self, request):
        self.request = request
        self.data = {}
        self.__parse(request)

    def __parse(self, request):
        path = request.path
        try:
            post_data = request.POST
            if post_data:
                data = post_data.dict()
                self.data = data
        except Exception as e:
            logger.error(f'[解析http post参数异常], path:{path}')

    def get_data(self) -> tuple | list | dict:
        return self.data


class ResponseStream:
    """
    返回文件流
    """

    def to_http_response(self, content_type: str = None, name: str = None) -> HttpResponse:
        if content_type is None:
            content_type = 'application/stream'

        if name is None:
            name = "stream.tmp"

        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{name}"'

        return response

    def excel_http_response(self, name: str = None) -> HttpResponse:
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return self.to_http_response(content_type=content_type, name=name)

    def query_set_to_excel_http_response(self, name: str = None, query_set: QuerySet = None,
                                         time_fields: list[str] = None, row_handler=None) -> HttpResponse:
        if time_fields is None:
            time_fields = ['create_time', 'update_time']

        if query_set is None:
            df_data = [[]]
        else:
            all_dtm = get_datetime_fields(query_set.model)
            time_fields = list(tuple(all_dtm))
            df_data = list(query_set.values())

        df = pd.DataFrame(df_data)
        if name is None:
            name = "stream.tmp"

        response = self.excel_http_response(name=name)
        for time_field in time_fields:
            if time_field in df.columns:
                try:
                    # 将带时区的日期时间转换为无时区的日期时间
                    df[time_field] = df[time_field].apply(lambda x: x.tz_localize(None) if x is not None else x)
                    # non_null_mask = df[time_field].notna()
                    # df.loc[non_null_mask, time_field] = df.loc[non_null_mask, time_field].dt.tz_localize(None)
                except Exception as e:
                    logger.error(f'[pandas转换时区异常]', exc_info=True)

        if row_handler:
            row_handler(pd)
        df.to_excel(response, index=False, engine='openpyxl')
        return response
