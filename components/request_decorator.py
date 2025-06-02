"""request 装饰器"""
from typing import Callable, Union

from common.auth_params import auth_user_params
from common.constants import UserParamsConstant
from common.exts import PermiError
from components.cache_singleton import DjangoRedisCacheSingleton
from system.user.permission_services import get_role_permission, get_menu_permission


@auth_user_params()
def user_id(user_id=None):
    return user_id


@auth_user_params(userid_cache_key=UserParamsConstant.USERNAME_KEY)
def username(username=None):
    return username


@auth_user_params(userid_cache_key=UserParamsConstant.USER_KEY)
def user_data(user_data=None):
    return user_data


@auth_user_params(userid_cache_key=UserParamsConstant.JWT_UUID_KEY)
def user_token_uuid(cache_uuid=None):
    return cache_uuid


dj_redis_cache = DjangoRedisCacheSingleton()

@dj_redis_cache.instance.cache_decorator(key_prefix="cache:user:permis", cache_key="token_uuid")
def __get_user_all_permis(token_uuid):
    """获取所有权限"""
    _user_id = user_id()
    _username = username()
    roles = get_role_permission(user_id=_user_id, username=_username)
    permissions = get_menu_permission(user_id=_user_id, username=_username, roles=roles)
    return permissions


def get_user_all_permis():
    """获取当前用户所有权限"""
    token_uuid = user_token_uuid()
    return __get_user_all_permis(token_uuid=token_uuid)


def clear_user_all_permis():
    """情况用户权限缓存"""
    return dj_redis_cache.instance.del_join_keys(["cache:user:permis", "token_uuid", f"{user_token_uuid()}"])


def has_permis(perims: Union[list[str], str] = None, apply: str = 'and'):
    """权限装饰器"""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if perims is None:
                raise PermiError("配置错误, 没有操作权限")

            if isinstance(perims, str) and not perims:
                raise PermiError("配置错误, 没有操作权限")

            if isinstance(perims, list) and len(perims) == 0:
                raise PermiError("配置错误, 没有操作权限")

            all_permis = get_user_all_permis()
            if all_permis is None or len(all_permis) == 0:
                raise PermiError("没有操作权限")

            if isinstance(perims, str):
                if perims not in all_permis:
                    raise PermiError("当前没有操作权限")
            else:
                if len(perims) == 1:
                    if perims[0] not in all_permis:
                        raise PermiError("当前没有操作权限")
                    else:
                        ret_flag = False
                        for perim in perims:
                            if perim not in all_permis:
                                ret_flag = True

                        if ret_flag is True:
                            raise PermiError("当前没有操作权限")

            return func(*args, **kwargs)

        return wrapper

    return decorator
