# middleware.py
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin


class JsonServerErrorMiddleware(MiddlewareMixin):

    def process_response(self, request, response=None):
        if isinstance(response, (PermissionDenied, SuspiciousOperation)):
            return response  # 不处理这些异常，让 Django 的默认处理机制处理它们
        elif isinstance(response, HttpResponseNotFound):
            return JsonResponse({
                'code': 404,
                'msg': 'The requested resource was not found.',
                'path': request.path
            }, status=404)
        elif isinstance(response, HttpResponseServerError):
            return JsonResponse({
                'code': 500,
                'msg': f'{response.content.decode("utf-8")}',
                'path': request.path
            }, status=500)
        return response  # 其他异常，不处理或按需处理
