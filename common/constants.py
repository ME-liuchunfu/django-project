"""
常量配置
"""


class HttpParamsConstant:
    """http 常量"""
    SERVER_URL = "server_url"
    STATIC_URL = "static_url"
    HTTP_AUTHORIZATION = "HTTP_AUTHORIZATION"
    BEARER = "Bearer"
    TOKENENCRYPT = "tokenEncrypt"
    TOKENENCRYPT_KEY = "tokenEncryptKey"
    SECRETKEY = "secretkey"
    ENCRYPT = "encrypt"
    AUTH_USER_DATA = "auth_data"
    USER_ID = "user_id"


class UserParamsConstant:
    """用户 常量"""
    PARAMS = "params"
    USERNAME = "username"
    PASSWORD = "password"
    USER_ID_KEY = "user_id"
    USER_KEY = "user_data"
    USERNAME_KEY = "username"

    JWT_UUID_KEY = "cache_uuid"




class ThreadParamsConstant:
    """线程 常量"""
    CURRENT_REQUEST = "current_request"


LOGGER_THREAD_POOL = "LOGGING_EXECUTOR"

HTTP_USER_AGENT = "HTTP_USER_AGENT"

IP_PARSE_URLS = "IP_PARSE_URLS"
IP_PARSE_SWITCH_ON = "switchOn"
IP_PARSE = "IP_PARSE"


class JwtParamsConstant:

    JWT_EXP = "exp"

    TOKEN_FLUSH_CONF = "TOKEN_FLUSH_CONF"
    TOKEN_FLUSH_CONF_TIME = "time"
    TOKEN_FLUSH_CONF_EXP_TIME = "exp_time"
    TOKEN_FLUSH_RESPONSE_HEADER_KEY = "flush_token"