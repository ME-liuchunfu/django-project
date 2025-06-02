import json
import logging

from django_redis.serializers.base import BaseSerializer


logger = logging.getLogger(__name__)

class StringSerializer(BaseSerializer):
    """直接存储和读取字符串的序列化器"""

    def dumps(self, value):
        # 确保值是字符串
        if not isinstance(value, str):
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        return value

    def loads(self, value):
        # 直接返回字符串
        if value is None:
            return None

        try:
            return json.loads(value)
        except Exception as e:
            logger.error(f'解析redis json错误', exc_info=e)

        return value

