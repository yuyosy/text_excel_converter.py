import re
from pathlib import Path
from typing import List, Tuple, Union

from dataobject.data_object import DataObject

from .const import FILE_DATETIME_FORMAT


def replace_inner_params(placeholder: str, data: DataObject) -> str:
    for item in re.findall(r'@\{.+?\}', placeholder):
        replaceto = val if (val := data.get(item[2:-1])) else ''
        placeholder = placeholder.replace(item, replaceto)
    return placeholder


def replace_datetime_to_placeholder(filename: str, *, format: str = FILE_DATETIME_FORMAT) -> Tuple[str, Union[str, None]]:
    format = format if format else FILE_DATETIME_FORMAT
    replace_list: List[Tuple[str, str]] = [
        ('%Y', r'[12]\d{3}'),
        ('%y', r'\d{2}'),
        ('%m', r'(0[1-9]|1[0-2])'),
        ('%d', r'(0\d|[12]\d|3[01])'),
        ('%H', r'([01]\d|2[0-3])'),
        ('%I', r'(0\d|1[0-2])'),
        ('%M', r'([0-5]\d)'),
        ('%S', r'([0-5]\d)'),
        ('%p', r'(AM|PM)')
    ]
    for tar, repl in replace_list:
        format = format.replace(tar, repl)
    placeholder = re.search(format, filename)
    if placeholder is None:
        return filename, None
    return re.sub(format, '${generate_datetime}', filename), placeholder.group()


def remove_invalid_charactor(placeholder: str) -> str:
    placeholder = re.sub(r'[\\/:*?"<>|]', '', placeholder)
    return placeholder


def rename_duplicate_filename(path: Path, *, counter=1) -> Path:
    if path.exists():
        if matched := re.search(r'\(\d+\)$', path.stem):
            counter = int(matched.group()[1:-1]) + 1
        renamed = re.sub(r'\(\d+\)$', f'({counter}){path.suffix}', path.stem)
        return rename_duplicate_filename(path.with_name(renamed))
    return path
