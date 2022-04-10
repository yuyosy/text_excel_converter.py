from pathlib import Path
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


def rename_duplicate_filename(path:Path, *, counter = 1) -> Path:
    if path.exists():
        if matched := re.search(r'\(\d+\)$', path.stem):
            counter = int(matched.group()[1:-1]) + 1
        renamed = re.sub(r'\(\d+\)$', f'({counter}){path.suffix}', path.stem)
        return rename_duplicate_filename(path.with_name(renamed))
    return path
