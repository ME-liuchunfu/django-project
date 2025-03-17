from encodings.utf_8_sig import encode
from sys import prefix

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings
import logging

from common.cryption import cryption
from common.http import AjaxJsonResponse

logger = logging.getLogger(settings.APP_LOGGER_NAME)



class JwtAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        white_url_dist = settings.WHITE_URL_DIST
        if not ((white_list := white_url_dist.get("server_url")) and white_list and len(white_list) > 0):
            white_list = []
            logger.warning("setting.py文件未配置WHITE_URL_DIST白名单配置，格式:WHITE_URL_DIST = {'server_url':[xxx], 'static_url':[xxx]}")

        if not ((static_url_list := white_url_dist.get("static_url")) and static_url_list and len(static_url_list) > 0):
            static_url_list = []

        path = request.path
        if startWithUri(static_url_list=static_url_list, path=path):
            logger.debug("[静态资源放行] request static path: %s", path)
            return None
        if path not in white_list:
            token = request.META.get('HTTP_AUTHORIZATION')
            logger.info("[授权认证] request path: %s ,token=%s", path, token)
            try:
                prefix = "Bearer "
                if token.startswith(prefix):
                    token = token[len(prefix):]

                # 先解密，后解jwt
                LOGIN_WEB_CONF = settings.LOGIN_WEB_CONF
                tokenEncrypt = LOGIN_WEB_CONF.get("tokenEncrypt")
                if tokenEncrypt:
                    tokenEncryptKey = LOGIN_WEB_CONF.get("tokenEncryptKey")
                    token = cryption.aes_decrypt_data(encrypted=token, key=tokenEncryptKey)

                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                decode_data = jwt_decode_handler(token)
                # 授权后的信息放到request域
                request.auth_data = decode_data
            except ExpiredSignatureError:
                logger.warning("[token认证过期] request path: %s , token=%s", path, token, exc_info=True)
                return AjaxJsonResponse(code=401, msg='Token过期，请重新登录！')
            except InvalidTokenError:
                logger.warning("[token认证失败] request path: %s , token=%s", path, token, exc_info=True)
                return AjaxJsonResponse(code=401, msg='Token验证失败！')
            except PyJWTError:
                logger.warning("[token认证异常] request path: %s , token=%s", path, token, exc_info=True)
                return AjaxJsonResponse(code=401, msg='Token验证异常！')
            except Exception:
                logger.warning("[token认证异常] request path: %s , token=%s", path, token, exc_info=True)
                return AjaxJsonResponse(code=500, msg='Token验证异常！')

        else:
            logger.debug("[不需要token验证] request path: %s", path)
            return None


def startWithUri(static_url_list: list[str], path: str = None) -> bool:
    """
    从static_url_list中的每一项匹配 path，
    如果path是static_url_list某一项开头则放行：true
    否则false
    """
    if not path:
        return False

    if static_url_list and len(static_url_list) > 0:
        for url in static_url_list:
            if path.startswith(url):
                return True
    return False