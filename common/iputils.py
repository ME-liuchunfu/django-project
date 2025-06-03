"""
ip 工具类
"""


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

