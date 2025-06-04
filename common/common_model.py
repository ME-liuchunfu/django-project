"""基础模块"""
import json
from typing import Optional, Any


class BaseDict(dict):
    """基础字典类"""
    
    def __init__(self, *args, **kwargs):
        super(BaseDict, self).__init__(*args, **kwargs)


    def to_dict(self) -> dict:
        """转换为新的字典对象"""
        return dict(self)

    def to_int(self, val: Optional[Any] = None) -> Optional[int]:
        if val is not None:
            ret = self.get(val, None)
            if ret is not None:
                return int(ret)

        return None

    def to_bool(self, val: Optional[Any] = None) -> bool:
        if val is not None:
            ret = self.get(val, None)
            if ret is not None:
                return bool(ret)

        return False

    def to_str(self, val: Optional[Any] = None) -> Optional[str]:
        if val is not None:
            ret = self.get(val, None)
            if ret is not None:
                return str(ret)

        return None

    def json_dumps(self) -> str:
        """转成json字符串"""
        return json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'), ensure_ascii=False)


    def set_val(self, key, val=None):
        """设置值"""
        if val is not None:
            self[key] = val