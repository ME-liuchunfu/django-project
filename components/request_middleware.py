"""request 域"""
from django.http import HttpRequest

from common.constants import ThreadParamsConstant
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