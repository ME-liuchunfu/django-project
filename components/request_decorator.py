"""request 装饰器"""
from common.auth_params import auth_user_params
from common.constants import UserParamsConstant


@auth_user_params()
def user_id(user_id=None):
    return user_id


@auth_user_params(userid_cache_key=UserParamsConstant.USERNAME_KEY)
def username(username=None):
    return username


@auth_user_params(userid_cache_key=UserParamsConstant.USER_KEY)
def user_data(user_data=None):
    return user_data