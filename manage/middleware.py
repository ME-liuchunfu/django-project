# middleware.py
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin


class JsonServerErrorMiddleware(MiddlewareMixin):

    def process_response(self, request, exception):
        if isinstance(exception, (PermissionDenied, SuspiciousOperation)):
            return None  # 不处理这些异常，让 Django 的默认处理机制处理它们
        elif isinstance(exception, HttpResponseNotFound):
            return JsonResponse({
                'code': 404,
                'msg': 'The requested resource was not found.',
                'path': request.path
            }, status=404)
        elif isinstance(exception, HttpResponseServerError):
            return JsonResponse({
                'code': 500,
                'msg': f'{exception.content.decode("utf-8")}',
                'path': request.path
            }, status=500)
        return None  # 其他异常，不处理或按需处理
