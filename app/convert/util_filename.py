import re
from dataobject.data_object import DataObject


def replace_inner_params(placeholder: str, data: DataObject) -> str:
    for item in re.findall(r'@\{.+?\}', placeholder):
        replaceto = val if (val := data.get(item[2:-1])) else ''
        placeholder = placeholder.replace(item, replaceto)
    return placeholder


def remove_invalid_charactor(placeholder: str) -> str:
    placeholder = re.sub(r'[\\/:*?"<>|]', '', placeholder)
    return placeholder

