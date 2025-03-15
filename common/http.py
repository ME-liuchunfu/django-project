import json
import logging

from django.http import JsonResponse, QueryDict, HttpResponse

logger = logging.getLogger(__name__)


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


class ParseRequestMetaUser:
    """
    解析jwt授权用户信息
    数据类型：dict
    {
        'user_id': int,
        'username': str,
        'exp': int 过期时间,
        'email': str
    }
    """

    def __init__(self, request):
        self.user = {}
        self.__parse(request)

    def __parse(self, request):
        auth_data = None
        try:
            if hasattr(request, "auth_data"):
                auth_data = request.auth_data
                self.user.update(auth_data)
        except Exception as e:
            logger.error(f'[http授权解析参数错误], {auth_data}', exc_info=True)

    def __call__(self):
        return self.user

    def get_userid(self) -> int:
        return self.user.get("user_id")

    def get_username(self) -> str:
        return self.user.get("username")


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

