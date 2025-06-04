"""
日志记录装饰器
"""

import inspect
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Union
from django.http import JsonResponse, HttpRequest

from common.constants import LOGGER_THREAD_POOL
from common.http import RequestGetParams, RequestPostParams, RequestBody
from common.iputils import get_client_ip, get_real_address_by_ip
from common.request_storage import get_current_request
from components.request_decorator import get_dept_name, username
from manage import settings
from monitor.operlog.services import OperLogService

logger = logging.getLogger(__name__)


class OperatorType(Enum):
    """操作人类别"""
    # 其它
    OTHER = 0
    # 后台用户
    MANAGE = 1
    # 手机端用户
    MOBILE = 2


class BusinessType(Enum):
    """业务操作类型"""

    # 其它
    OTHER = 0
    # 新增
    INSERT = 1

    # 修改
    UPDATE = 2

    # 删除
    DELETE = 3

    # 授权
    GRANT = 4

    # 导出
    EXPORT = 5

    # 导入
    IMPORT = 6

    # 强退
    FORCE = 7

    # 生成代码
    GENCODE = 8

    # 清空数据
    CLEAN = 9


def parse_request_param(req) -> str:
    try:
        if req.method.upper() == 'GET':
            req_data = RequestGetParams(req).get_data()
        elif req.method.upper() == 'put':
            req_data = RequestBody(req).get_data()
        else:
            req_data = RequestPostParams(req).get_data()
        oper_param = to_json(req_data)
        return oper_param
    except Exception as xe:
        logger.error(f'获取请求参数错误', exc_info=True)

    return ''


def log_async_logger(
    title = "",
    business_type: Union[int, BusinessType] = BusinessType.OTHER,
    operator_type: Union[int, OperatorType] = OperatorType.MANAGE,
    executor = LOGGER_THREAD_POOL,
    save_request_data: bool = True,
    save_response_data: bool = True,
    exclude_param_names: list[str] = None
):
    """异步日志装饰器，支持指定线程池"""

    if isinstance(business_type, BusinessType):
        business_type = business_type.value

    if isinstance(operator_type, OperatorType):
        operator_type = operator_type.value

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # loop = asyncio.get_event_loop()
            thread_pool: ThreadPoolExecutor = getattr(settings, executor)
            method_name = func.__name__
            request_method = 'none'
            oper_ip = ''
            dept_name = ''
            oper_name = ''
            oper_url = ''
            oper_location = ''
            oper_param = ''
            error = None
            result = None
            start_time = current_millis()
            end_time = start_time
            status = 0
            try:
                result = func(*args, **kwargs)
                end_time = current_millis()

                req = get_current_request()
                request_method = req.method
                oper_ip = get_client_ip(req)
                dept_name = get_dept_name()
                oper_name = username()
                # oper_url = req.build_absolute_uri()
                oper_url = req.get_full_path()

                if save_request_data:
                    oper_param = parse_request_param(req)

            except Exception as e:
                logger.error(f'执行错误:method:{func.__name__}', exc_info=True)
                status = 1
                error = e

            json_result = ''
            if save_response_data:
                json_result = to_json(result)

            cost_time = end_time - start_time

            # 异步记录成功日志
            def log():
                error_msg = ''
                if error is not None:
                    error_msg = str(error)

                oper_location = get_real_address_by_ip(oper_ip)
                OperLogService().insert_oper(
                    title=title, business_type=business_type, operator_type=operator_type,
                    method_name=method_name, request_method=request_method, oper_name=oper_name,
                    oper_ip=oper_ip, status=status,
                    dept_name=dept_name, error_msg=error_msg,
                    oper_url=oper_url, oper_location=oper_location, oper_param=oper_param,
                    cost_time=cost_time, json_result=json_result
                )

            thread_pool.submit(log)
            # loop.run_in_executor(thread_pool, lambda: log())

            if error is not None:
                raise error

            return result

        return wrapper

    return decorator



def param_to_json(func, exclude_param_names, *args, **kwargs) -> str:
    try:
        # 获取函数签名
        sig = inspect.signature(func)
        # 绑定参数
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # 处理位置参数和关键字参数
        all_params = bound_args.arguments

        ret_dict = {}
        if exclude_param_names is None:
            ret_dict.update(all_params)
        else:
            for k, v in all_params.items():
                ret_dict[k] = v

        return to_json(ret_dict)
    except Exception as e:
        logger.error(f'获取请求参数错误', exc_info=True)
        return ''


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # 转为 ISO 格式字符串
        return super().default(obj)



def to_json(param) -> str:
    try:
        data = param
        if isinstance(param, JsonResponse):
            data = param.content
            if isinstance(data, bytes):
                data = data.decode(encoding="utf-8")

        if isinstance(data, str):
            return data

        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    except Exception as e:
        pass
    return ''


def current_millis() -> int:
    """
    返回当前时间的毫秒级时间戳（整数）
    等价于 Java 的 System.currentTimeMillis()
    """
    return int(time.time() * 1000)

