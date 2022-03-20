import re
from datetime import datetime
from enum import Flag, auto
from typing import Any, Dict


class FormatType(Flag):
    PASS = auto()

def marshalling(value: str, format:Dict[str, Any]) -> Any:
    if isinstance(format, str):
        return value
    elif isinstance(format, dict):
        f = format.get('format')
        if isinstance(f, dict) and value is None:
            return None
        elif isinstance(f, dict) and value:
            for name, match in f.items():
                return marshalling_format_action(name, match, value)
        elif f == 'int':
                return int(value) if value else value
        elif f == 'float':
                return float(value) if value else value
        elif f == 'string':
                return str(value) if value else value
        

def marshalling_format_action(name:str, match:Any, value:Any) -> Any:
    if name == 'dict' and match == value:
        return re.split(match, value)
    elif name == 'pass' and match == value:
        return FormatType.PASS
    elif name == 'true' and match == value:
        return True
    elif name == 'false' and match == value:
        return False
    elif name == 'none' and match == value:
        return None
    elif name == 'datetime' and value:
        return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S' if match is None else match)
    return value
    