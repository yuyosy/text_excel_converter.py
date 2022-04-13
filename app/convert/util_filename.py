import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Union

from dataobject.data_object import DataObject

from .class_definitions import DefinitionsData
from .class_metadata import Metadata
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


def setup_filename_placeholder(definition_data: DefinitionsData, data: DataObject) -> str:
    placeholder = fn if (fn := definition_data.output_filename) else '${source_basename}${generate_datetime}'
    placeholder = replace_inner_params(placeholder, data)
    placeholder = remove_invalid_charactor(placeholder)
    return placeholder


def sourcepath_to_placeholder(path: Union[Path, str], datetime_format: str = '') -> str:
    if isinstance(path, Path):
        name = path.stem
    else:
        i = path.rfind('.')
        if 0 < i < len(path) - 1:
            name = path[:i]
        else:
            name = path
    format = datetime_format if datetime_format else FILE_DATETIME_FORMAT
    filename, matched = replace_datetime_to_placeholder(name, format=format)
    return filename


def placeholder_to_savename(tmpl_placeholder: str, src_placeholder: str, include_datetime: bool = True) -> str:
    if not include_datetime:
        tmpl_placeholder.replace('${generate_datetime}', '')
    savename = tmpl_placeholder
    savename = savename.replace('${source_basename}', src_placeholder.replace('${generate_datetime}', ''))
    return savename


def set_savename_datetime(savename: str, metadata: Metadata, datetime_format: str = '') -> str:
    format = datetime_format if datetime_format else FILE_DATETIME_FORMAT
    if '${generate_datetime}' in savename:
        dt = datetime.now()
        dt_gen_excel = metadata.datetime_generated_excel
        dt_gen_text = metadata.datetime_generated_text
        if dt_gen_text and dt_gen_excel:
            if dt_gen_excel.microsecond >= dt_gen_text.microsecond:
                dt = dt_gen_excel
            if dt_gen_excel.microsecond < dt_gen_text.microsecond:
                dt = dt_gen_text
        elif dt_gen_excel:
            dt = dt_gen_excel
        elif dt_gen_text:
            dt = dt_gen_text

        savename = savename.replace('${generate_datetime}', dt.strftime(format))
    return savename
