import json

from django.conf import settings
from django.views import View
from rest_framework_jwt.settings import api_settings

from common.cryption import cryption
from common.cryption.cryption import bcrypt_check_password
from common.http import AjaxJsonResponse, RequestBody, ParseJson, ParseRequestMetaUser
from system.models import SysUser
import logging

from system.user.services import get_routers

logger = logging.getLogger(__name__)


class LoginView(View):

    """
    登录授权
    """

    def post(self, request):
        username = None
        password = None
        try:
            LOGIN_WEB_CONF = settings.LOGIN_WEB_CONF
            LOGIN_WEB_SECRETKEY = LOGIN_WEB_CONF.get("secretkey")
            encrypt = LOGIN_WEB_CONF.get("encrypt") if 'encrypt' in LOGIN_WEB_CONF else False
            form_json = RequestBody(request)()
            encrypt_flag = form_json.get("encrypt")
            if encrypt and (not encrypt_flag or encrypt_flag != True):
                raise ValueError("参数错误")

            if encrypt:
                params = form_json.get("params")
                data = cryption.aes_decrypt_data(encrypted=params, key=LOGIN_WEB_SECRETKEY)
                data = ParseJson(data)()
                username = data.get("username")
                password = data.get("password")
            else:
                username = form_json.get("username")
                password = form_json.get("password")

            # code = data.get("code")
            # uuid = data.get("uuid")
            if not username or not password:
                raise ValueError("参数错误")
            user = self.__validata(username, password)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 将用户对象传递进去，获取到该对象的属性值
            payload = jwt_payload_handler(user)
            # 将属性值编码成jwt格式的字符串
            token = jwt_encode_handler(payload)

            # token进行二次加密
            tokenEncrypt = LOGIN_WEB_CONF.get("tokenEncrypt")
            if tokenEncrypt:
                tokenEncryptKey = LOGIN_WEB_CONF.get("tokenEncryptKey")
                token = cryption.aes_encrypt_data(token, key=tokenEncryptKey)

        except Exception as e:
            logger.error(f"[登录授权失败] username:{username}, password:{password}", exc_info=True)
            return AjaxJsonResponse(code=500, msg="授权失败")

        return AjaxJsonResponse(msg='success', extra_dict={'token':token})


    def __validata(self, username, password):
        try:
            user = SysUser.objects.filter(username=username).first()
            if not user:
                raise ValueError("账号存在")
            if user.status == '1':
                raise ValueError("账号停用")
            if not bcrypt_check_password(user.password, password):
                raise ValueError("账号密码不正确")
            return user
        except Exception as e:
            logger.error(f"[查询错误], username:{username}", exc_info=True)
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

        return AjaxJsonResponse(msg='success', extra_dict={'captchaEnabled':False, 'encrypt': False})


class LogoutView(View):

    def post(self, request):
        return AjaxJsonResponse(msg='success')


class RoutersView(View):

    """
    路由
    """

    def get(self, request):
        user_id = ParseRequestMetaUser(request).get_userid()
        menus_data = get_routers(user_id)
        return AjaxJsonResponse(msg='success', data=menus_data)