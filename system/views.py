import uuid

from django.conf import settings
from django.views import View
from rest_framework_jwt.settings import api_settings
from common.constants import HttpParamsConstant, UserParamsConstant
from common.cryption import cryption
from common.cryption.cryption import bcrypt_check_password
from common.http import AjaxJsonResponse, RequestBody, ParseJson
from components import request_decorator
from components.log_logininfor import record_logininfor, LogLoginInforType
from components.request_decorator import clear_user_all_permis, username
from system.models import SysUser
import logging
from system.user.permission_services import get_routers

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class LoginView(View):
    """
    登录授权
    """

    def post(self, request):
        username = None
        password = None
        try:
            LOGIN_WEB_CONF = settings.LOGIN_WEB_CONF
            LOGIN_WEB_SECRETKEY = LOGIN_WEB_CONF.get(HttpParamsConstant.SECRETKEY)
            encrypt = LOGIN_WEB_CONF.get(HttpParamsConstant.ENCRYPT, False)
            form_json = RequestBody(request)()
            encrypt_flag = form_json.get(HttpParamsConstant.ENCRYPT, False)
            if encrypt and (not encrypt_flag or encrypt_flag != True):
                raise ValueError("参数错误")

            if encrypt:
                params = form_json.get(UserParamsConstant.PARAMS)
                data = cryption.aes_decrypt_data(encrypted=params, key=LOGIN_WEB_SECRETKEY)
                data = ParseJson(data)()
                username = data.get(UserParamsConstant.USERNAME)
                password = data.get(UserParamsConstant.PASSWORD)
            else:
                username = form_json.get(UserParamsConstant.USERNAME)
                password = form_json.get(UserParamsConstant.PASSWORD)

            # code = data.get("code")
            # uuid = data.get("uuid")
            if not username or not password:
                raise ValueError("参数错误")
            user = self.__validata(username, password)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 将用户对象传递进去，获取到该对象的属性值
            payload = jwt_payload_handler(user)
            payload[UserParamsConstant.JWT_UUID_KEY] = f'permi:{user.user_id}:{uuid.uuid4().hex}'
            # 将属性值编码成jwt格式的字符串
            token = jwt_encode_handler(payload)

            # token进行二次加密
            token_encrypt = LOGIN_WEB_CONF.get(HttpParamsConstant.TOKENENCRYPT, True)
            if token_encrypt is True:
                token_encrypt_key = LOGIN_WEB_CONF.get(HttpParamsConstant.TOKENENCRYPT_KEY, '')
                token = cryption.aes_encrypt_data(token, key=token_encrypt_key)

            record_logininfor(req=request, username=payload.get(UserParamsConstant.USERNAME_KEY, ''),
                              status=LogLoginInforType.LOGIN_OK, message="登录成功")

        except Exception as e:
            logger.error(f"[登录授权失败] username:{username}, password:{password}", exc_info=True)
            record_logininfor(req=request, username=username,
                              status=LogLoginInforType.LOGIN_FAIL, message="登录授权失败")
            return AjaxJsonResponse(code=500, msg="授权失败")

        return AjaxJsonResponse(msg='success', extra_dict={'token': token})

    def __validata(self, username, password):
        try:
            user = SysUser.objects.filter(username=username).first()
            if not user:
                raise ValueError("账号不存在")
            if user.status == '1':
                raise ValueError("账号停用")
            if not bcrypt_check_password(user.password, password):
                raise ValueError("账号密码不正确")
            return user
        except Exception as e:
            logger.error(f"[查询错误], username:{username}", exc_info=False)
            raise ValueError('查询异常') from e


class CaptchaImageView(View):

    def get(self, request):
        LOGIN_WEB_CONF = settings.LOGIN_WEB_CONF
        encrypt = LOGIN_WEB_CONF.get("encrypt") if 'encrypt' in LOGIN_WEB_CONF else False
        if encrypt:
            LOGIN_WEB_SECRETKEY = LOGIN_WEB_CONF.get("secretkey")
            data = {
                'captchaEnabled': False,
                'secretkey': LOGIN_WEB_SECRETKEY,
                "encrypt": encrypt
            }
            return AjaxJsonResponse(msg='success', extra_dict=data)

        return AjaxJsonResponse(msg='success', extra_dict={'captchaEnabled': False, 'encrypt': False})


class LogoutView(View):

    def post(self, request):
        record_logininfor(req=request, username=username(),
                          status=LogLoginInforType.LOGOUT, message="登出成功")
        clear_user_all_permis()
        return AjaxJsonResponse(msg='success')


class RoutersView(View):
    """
    路由
    """

    def get(self, request):
        menus_data = get_routers(request_decorator.user_id())
        return AjaxJsonResponse(msg='success', data=menus_data)
