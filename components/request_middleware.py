"""request 域"""
import json

from django.http import HttpRequest, HttpResponse

from common.constants import ThreadParamsConstant
from common.exts import PermiError
from common.request_storage import _request_locals


class RequestMiddleware:
    """从request 获取用户数据"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # 将 request 存入线程局部变量
        _request_locals.current_request = request
        response = self.get_response(request)
        # 清理请求（避免内存泄漏）
        if hasattr(_request_locals, ThreadParamsConstant.CURRENT_REQUEST):
            del _request_locals.current_request

        return response


class ServiceExceptionMiddleware:
    """全局异常处理"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermiError):
            # 返回 JSON 格式的错误响应
            data = {
                "code": exception.code,
                "message": exception.msg
            }
            return HttpResponse(
                json.dumps(data),
                content_type="application/json",
                status=200
            )
        return None  # 其他异常由 Django 处理
