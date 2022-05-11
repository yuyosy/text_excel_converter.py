import re
from datetime import datetime
from enum import Flag, auto
from typing import Any, Dict, Tuple

from .const import DATETIME_FORMAT, DATETIME_FORMAT_HYPHEN


class FormatType(Flag):
    PASS = auto()


def marshalling(value: str, format: Dict[str, Any]) -> Any:
    if isinstance(format, str):
        return value
    elif isinstance(format, dict):
        f = format.get('format')
        if isinstance(f, dict) and value is None:
            return None
        elif isinstance(f, dict) and value:
            for name, tar in f.items():
                matched, val = marshalling_format_action(name, tar, value)
                if matched:
                    return val
            return value

        elif f == 'int':
            return int(value) if value else value
        elif f == 'float':
            return float(value) if value else value
        elif f == 'string':
            return str(value) if value else value
    return value


def marshalling_format_action(name: str, cell_val: Any, value: Any) -> Tuple[bool, Any]:
    if name == 'dict' and cell_val == value:
        return True, re.split(cell_val, value)
    elif name == 'pass' and cell_val == value:
        return True, FormatType.PASS
    elif name == 'true' and cell_val == value:
        return True, True
    elif name == 'false' and cell_val == value:
        return True, False
    elif name == 'none' and cell_val == value:
        return True, None
    elif name == 'datetime' and value:
        try:
            return True, datetime.strptime(str(value), DATETIME_FORMAT if cell_val is None else cell_val)
        except ValueError:
            return True, value
    return False, value


def unmarshalling(value: Any, format: Dict[str, Any]) -> Any:
    if isinstance(format, str):
        return value
    elif isinstance(format, dict):
        f = format.get('format')
        if isinstance(f, dict):
            for name, tar in f.items():
                matched, val = unmarshalling_format_action(name, tar, value)
                if matched:
                    return val
            return value
        elif f == 'int':
            return int(value) if value else value
        elif f == 'float':
            return float(value) if value else value
        elif f == 'string':
            return str(value) if value else value
    return value


def unmarshalling_format_action(name: str, cell_val: Any, value: Any) -> Tuple[bool, Any]:
    if name == 'dict' and cell_val == value:
        return True, str(value)
    elif name == 'pass' and value == FormatType.PASS:
        return True, cell_val
    elif name == 'true' and value == True:
        return True, cell_val
    elif name == 'false' and value == False:
        return True, cell_val
    elif name == 'none' and value == None:
        return True, cell_val
    elif name == 'datetime' and value:
        try:
            dt = datetime.strptime(str(value), DATETIME_FORMAT_HYPHEN)
            return True, dt.strftime(DATETIME_FORMAT if cell_val is None else cell_val)
        except ValueError:
            return True, value
    return False, value
