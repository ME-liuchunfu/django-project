"""授权函数"""
import inspect
from functools import wraps
from typing import Callable, Dict, Any, Union
from common.constants import UserParamsConstant, ThreadParamsConstant, HttpParamsConstant
from common.request_storage import get_current_request


def auth_user_params(userid_cache_key: str = None):
    """
    参数验证装饰器，用于检查函数参数是否为空并设置默认值

    Args:
        userid_cache_key: 用户id缓存键
    """
    if userid_cache_key is None:
        userid_cache_key = UserParamsConstant.USER_ID_KEY

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # 获取函数签名
            sig = inspect.signature(func)
            # 绑定参数
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # 处理位置参数和关键字参数
            all_params = bound_args.arguments

            cache_val = all_params.get(userid_cache_key, None)
            if cache_val is None:
                request = get_current_request()
                if request:
                    user_data = getattr(request, HttpParamsConstant.AUTH_USER_DATA, None)
                    if user_data:
                        all_params[userid_cache_key] = user_data.get(userid_cache_key, None)

            # 调用原始函数
            return func(**all_params)

        return wrapper

    return decorator

