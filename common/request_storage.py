# utils/request_storage.py
from threading import local
from common.constants import ThreadParamsConstant

# 创建线程安全的局部存储
_request_locals = local()


def get_current_request():
    """获取当前请求（仅在请求处理链中有效）"""
    return getattr(_request_locals, ThreadParamsConstant.CURRENT_REQUEST, None)

