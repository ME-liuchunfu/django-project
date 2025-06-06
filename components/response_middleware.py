"""
http response 中间件
"""
import logging
from datetime import datetime
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from common.constants import HttpParamsConstant, JwtParamsConstant
from common.cryption import cryption

logger = logging.getLogger(__name__)


class CustomTokenHeaderMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 处理请求前的逻辑（可选）

        # 获取响应对象
        response = self.get_response(request)

        try:
            token_dict = getattr(request, HttpParamsConstant.AUTH_USER_DATA)
            if token_dict is not None:
                exp = token_dict.get(JwtParamsConstant.JWT_EXP, None)
                if exp is not None:
                    now_seconds = int(datetime.now().timestamp())
                    token_conf = getattr(settings, JwtParamsConstant.TOKEN_FLUSH_CONF)
                    flush_time = int(5 * 60 * 60)
                    exp_time = int(2 * 60 * 60)
                    if token_conf is not None:
                        flush_time = int(token_conf.get(JwtParamsConstant.TOKEN_FLUSH_CONF_TIME, flush_time))
                        exp_time = int(token_conf.get(JwtParamsConstant.TOKEN_FLUSH_CONF_EXP_TIME, exp_time))

                    remain_time = int(exp - now_seconds)
                    if remain_time <= flush_time:
                        next_time = int(now_seconds + exp_time)
                        token_dict[JwtParamsConstant.JWT_EXP] = next_time
                        payload = dict(token_dict)
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                        token = jwt_encode_handler(payload)
                        # token进行二次加密
                        login_web_conf = settings.LOGIN_WEB_CONF
                        token_encrypt = login_web_conf.get(HttpParamsConstant.TOKENENCRYPT, True)
                        if token_encrypt is True:
                            token_encrypt_key = login_web_conf.get(HttpParamsConstant.TOKENENCRYPT_KEY, '')
                            token = cryption.aes_encrypt_data(token, key=token_encrypt_key)
                        response[JwtParamsConstant.TOKEN_FLUSH_RESPONSE_HEADER_KEY] = token
                        logger.info(f'response主动刷新token,过期时间:{parse_str_time(exp)},now:{parse_str_time(now_seconds)},'
                                    f'ramin:{remain_time},更新到:{parse_str_time(next_time)}')

        except Exception as e:
            logger.info(f'response刷新token异常，下次在检测')

        return response


def parse_str_time(sec: int)->str:
    try:
        dt_object = datetime.fromtimestamp(sec)
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time
    except:
        pass
    return ''