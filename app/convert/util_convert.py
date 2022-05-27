import re
from typing import Any, Dict

from dataobject.data_object import DataObject


def get_key(format: Dict[str, Any]) -> str:
    if isinstance(format, str):
        return format
    elif isinstance(format, dict):
        return format.get('key')
    return format


def get_key_list(data: Dict[str, Any]) -> Dict[str, str]:
    return {get_key(data.get(item)): item for item in data}


def overwrite(option: Dict[str, Any], value: Any, data: DataObject) -> bool:
    if isinstance(option, dict) and (opt := option.get('overwrite', None)):
        mode = opt.get('mode', None)
        string = opt.get('string', '')

        for param in re.findall(r'@\{.+?\}', string):
            replaceto = val if (val := data.get(param[2:-1])) else ''
            string = string.replace(param, replaceto)
        if (mode == 'not-eq' and string == value) or (mode == 'eq' and string != value):
            return False
    return True
