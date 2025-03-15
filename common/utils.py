import re
from typing import Any


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    # 将第一个单词保持原样，后续单词首字母大写
    return components[0] + ''.join(x.capitalize() for x in components[1:])



def keys_to_camel(d: Any) -> Any:
    """
    属性转驼峰
    """

    if isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            new_key = snake_to_camel(key)
            if isinstance(value, dict):
                new_dict[new_key] = keys_to_camel(value)
            elif isinstance(value, list):
                new_dict[new_key] = [keys_to_camel(item) if isinstance(item, (dict, list)) else item for item in value]
            else:
                new_dict[new_key] = value
        return new_dict
    elif isinstance(d, list):
        return [keys_to_camel(item) if isinstance(item, (dict, list)) else item for item in d]
    return d


def camel_to_snake(name):
    """
    将驼峰命名转换为下划线命名
    :param name: 驼峰命名的字符串
    :return: 下划线命名的字符串
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def keys_to_snake(d):
    """
    将字典的键从驼峰命名转换为下划线命名
    :param d: 输入的字典或列表
    :return: 转换后的字典或列表
    """
    if isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            new_key = camel_to_snake(key)
            if isinstance(value, dict):
                new_dict[new_key] = keys_to_snake(value)
            elif isinstance(value, list):
                new_dict[new_key] = [keys_to_snake(item) if isinstance(item, (dict, list)) else item for item in value]
            else:
                new_dict[new_key] = value
        return new_dict
    elif isinstance(d, list):
        return [keys_to_snake(item) if isinstance(item, (dict, list)) else item for item in d]
    return d


def is_not_empty(value: Any) -> bool:
    if not value:
        return False

    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        return len(value) > 0
    if isinstance(value, str):
        return len(value.strip()) > 0

    return True