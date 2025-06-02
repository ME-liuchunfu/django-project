# utils/request_storage.py
from threading import local

# 创建线程安全的局部存储
_request_locals = local()