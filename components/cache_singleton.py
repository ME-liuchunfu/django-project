import json
import logging
from django.core.cache import cache
from functools import wraps
from typing import Any, Optional, Callable

logger = logging.getLogger(__name__)


class DjangoRedisCacheSingleton:
    """
    Django-Redis 单例缓存类
    封装 django.core.cache 提供统一缓存接口
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instance._initialized = False
            cls.instance._create()
        return cls.instance

    def _create(self, cache_alias: str = "default"):
        if self._initialized:
            return
        self.cache_alias = cache_alias
        self._cache = cache
        self._initialized = True

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        val = self._cache.get(key, default)
        return val

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """设置缓存值"""
        return self._cache.set(key, value, timeout)

    def delete(self, key: str) -> int:
        """删除缓存项"""
        return self._cache.delete(key)

    def exists(self, key: str) -> bool:
        """检查缓存项是否存在"""
        return self._cache.has_key(key)  # Django 3.2及以下使用 has_key()

    def clear(self) -> None:
        """清空所有缓存"""
        self._cache.clear()

    def get_or_set(self, key: str, default: Callable, timeout: Optional[int] = None) -> Any:
        """获取缓存值，不存在时设置默认值"""
        return self._cache.get_or_set(key, default, timeout)

    def incr(self, key: str, delta: int = 1) -> int:
        """原子性自增操作"""
        return self._cache.incr(key, delta)

    def cache_decorator(self,
                        timeout: int = 3600,
                        key_prefix: str = "cache",
                        cache_key: Optional[str] = None):
        """
        缓存装饰器，用于缓存函数返回值

        Args:
            timeout: 缓存超时时间（秒）
            key_prefix: 缓存键前缀
            cache_key: str 二级缓存键
        """

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键（key_prefix和cache_key）
                result = None
                redis_key = None
                try:
                    redis_key = f"{key_prefix}"
                    if cache_key is not None and cache_key in kwargs:
                        id = kwargs.get(cache_key)
                        redis_key = f"{key_prefix}:{cache_key}:{str(id)}"

                    # 尝试从缓存获取
                    result = self.get(redis_key)
                    if result is not None:
                        return result

                    # 执行函数并缓存结果
                    result = func(*args, **kwargs)
                    self.set(redis_key, result, timeout)
                except Exception as e:
                    logger.error(f'获取缓存错误 method: {func.__name__}, redis_key: {redis_key}', exc_info=e)

                return result

            return wrapper

        return decorator


    def clear_cache_decorator(self,
                        key_prefix: str = "cache",
                        cache_key: Optional[str] = None):
        """
        缓存装饰器，用于清空缓存函数返回值

        Args:
            timeout: 缓存超时时间（秒）
            key_prefix: 缓存键前缀
            cache_key: str 二级缓存键
        """

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键（key_prefix和cache_key）
                result = None
                redis_key = None
                try:
                    redis_key = f"{key_prefix}"
                    if cache_key is not None and cache_key in kwargs:
                        id = kwargs.get(cache_key)
                        redis_key = f"{key_prefix}:{cache_key}:{str(id)}"

                    # 执行函数并缓存结果
                    result = func(*args, **kwargs)
                    self.delete(redis_key)
                except Exception as e:
                    logger.error(f'删除缓存错误 method: {func.__name__}, redis_key: {redis_key}', exc_info=e)

                return result

            return wrapper

        return decorator

    def del_join_keys(self, keys: list[str]):
        del_key = ":".join(keys)
        return self.delete(del_key)

    def batch_get(self, keys: list) -> dict:
        """批量获取缓存值"""
        return self._cache.get_many(keys)

    def batch_set(self, data: dict, timeout: Optional[int] = None) -> None:
        """批量设置缓存值"""
        self._cache.set_many(data, timeout)



