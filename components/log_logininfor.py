"""
登录日志
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Union

from django.utils import timezone

from common.constants import LOGGER_THREAD_POOL, HTTP_USER_AGENT
from common.iputils import get_client_ip, get_real_address_by_ip
from common.user_agents_utils import parse_useragent
from manage import settings
from monitor.logininfor.services import LogininforService

logger = logging.getLogger(__name__)


class LogLoginInforType(Enum):

    # 注销
    LOGOUT = "Logout"
    # 注册
    REGISTER = "Register"
    # 登录失败
    LOGIN_FAIL = "Error"

    LOGIN_OK = "LoginOk"



def record_logininfor(
    req=None,
    username = "",
    status: Union[str, LogLoginInforType] = "",
    message: str = "",
    params: Union[list[str], tuple[str], str] = None
):
    try:
        thread_pool: ThreadPoolExecutor = getattr(settings, LOGGER_THREAD_POOL)
        user_agent = parse_useragent(req.META.get(HTTP_USER_AGENT, ''))
        ipaddr = get_client_ip(req)
        login_location = get_real_address_by_ip(ipaddr)

        if isinstance(status, LogLoginInforType):
            if status == LogLoginInforType.LOGIN_FAIL:
                status = "1"
            else:
                status = "0"

        log_msg = ''
        if params is not None:
            if isinstance(params, list) or isinstance(params, tuple):
                log_msg = "|".join(params)
            else:
                log_msg = params

        logger.info(f'[{ipaddr}][{username}][{status}][{message}]{log_msg}')

        def log():
            LogininforService().insert_logininfo(
                user_name=username, ipaddr=ipaddr, login_location=login_location,
                browser=user_agent.browser, os_name=user_agent.os, status=status,
                msg=message, login_time=timezone.now(),
            )

        thread_pool.submit(log)
    except Exception as e:
        logger.info(f'记录登录日志异常,username:{username},status:{status},message:{message}', exc_info=True)