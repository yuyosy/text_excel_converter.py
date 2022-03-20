from typing import Any, Dict, List


def get_key(format: Dict[str, Any]) -> str:
    if isinstance(format, str):
        return format
    elif isinstance(format, dict):
        return format.get('key')
    return format


def get_key_list(data: Dict[str, Any]) -> Dict[str, str]:
    return {get_key(data.get(item)): item for item in data}
