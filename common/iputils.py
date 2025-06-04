"""
ip 工具类
"""
import ipaddress
import logging
import random

import requests
from django.conf import settings
from common.constants import IP_PARSE, IP_PARSE_SWITCH_ON, IP_PARSE_URLS

logger = logging.getLogger(__name__)


def get_client_ip(request, trusted_proxies=None):
    """
    获取客户端的真实 IP 地址，支持代理服务器和多级代理

    参数:
        request: Django 的 HttpRequest 对象
        trusted_proxies: 可信代理服务器的 IP 地址列表或集合

    返回:
        客户端的真实 IP 地址 (字符串)
    """
    # 设置默认的可信代理
    if trusted_proxies is None:
        trusted_proxies = set()
    elif isinstance(trusted_proxies, list):
        trusted_proxies = set(trusted_proxies)

    # 尝试从常见的代理头中获取 IP
    possible_headers = [
        'HTTP_CF_CONNECTING_IP',  # Cloudflare
        'HTTP_X_REAL_IP',  # Nginx
        'HTTP_X_FORWARDED_FOR',  # 通用代理
    ]

    for header in possible_headers:
        value = request.META.get(header)
        if value:
            if header == 'HTTP_X_FORWARDED_FOR':
                # 处理 X-Forwarded-For 格式: client_ip, proxy1, proxy2...
                ips = [ip.strip() for ip in value.split(',')]
                # 从右向左遍历，找到第一个不在可信代理列表中的 IP
                for ip in reversed(ips):
                    if ip not in trusted_proxies:
                        return ip
                # 如果所有 IP 都在可信列表中，返回最左侧的 IP（客户端 IP）
                return ips[0]
            else:
                # 其他头通常直接包含客户端 IP
                return value

    # 如果没有找到代理头，返回直接连接的 IP
    return request.META.get('REMOTE_ADDR', 'unknown')


def is_private_ip(ip: str) -> bool:
    """
    判断给定的 IP 地址是否为内网地址

    参数:
        ip (str): 需要判断的 IP 地址字符串

    返回:
        bool: 如果是内网地址返回 True，否则返回 False
    """
    try:
        # 解析 IP 地址
        ip_obj = ipaddress.ip_address(ip)
        # 判断是否为私有地址
        return ip_obj.is_private
    except ValueError as e:
        # 处理无效 IP 地址的情况
        logger.error(f"错误: 无效的 IP 地址 - {ip}", exc_info=True)
        return False


def get_real_address_by_ip(ip: str) -> str:
    """通过ip解析地址"""
    ret = "XX XX"
    try:
        if is_private_ip(ip):
            ret = "内网IP"
        else:
            ip_parse = getattr(settings, IP_PARSE)
            switch_on = ip_parse.get(IP_PARSE_SWITCH_ON, False)
            if switch_on is True:
                urls = ip_parse.get(IP_PARSE_URLS, [])
                if len(urls) > 0:
                    url = random.choice(urls)
                    response = requests.get(url=f"{url}?ip={ip}&json=true")
                    if response.status_code == 200:
                        json_data = response.json()
                        ret = f"{json_data.get('pro', '')} {json_data.get('city', '')}"

    except Exception as e:
        logger.error(f'ip地址解析异常,ip:{ip}', exc_info=True)

    return ret

