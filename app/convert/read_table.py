
from typing import Any, Iterator, List, Tuple

from openpyxl.workbook.workbook import Workbook

from .class_definitions import Definitions
from .escape_str import escape_str
from .marshal_data_format import FormatType, marshalling
from .util_convert import get_key_list
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def read_table(workbook: Workbook, definitions: Definitions) -> Iterator[Tuple[str, Any]]:
    sheet = workbook[definitions.sheet]
    key_list = get_key_list(definitions.data)

    min_col, max_col = to_columns_indexes_tuple(definitions.columns)
    key_col = to_relative_column_index(0 if (c := definitions.key_col) is None else c, min_col)
    val_col = to_relative_column_index(0 if (c := definitions.value_col) is None else c, min_col)
    header_row = 0 if (c := definitions.header_row) is None else c
    begin_row = 0 if (c := definitions.begin_row) is None else c

    header = [col.value for col in sheet[header_row][min_col-1:max_col]]

    for row in sheet.iter_rows(min_row=begin_row, min_col=min_col, max_col=max_col):
        if not any(cell.value for cell in row):
            break
        key_cell = row[key_col]
        if not key_cell.value:
            continue
        items: List[Tuple[str, Any]] = []
        for head, item in zip(header, row):
            header_key = key_list.get(head, '')
            if not header_key:
                continue
            items.append((header_key, marshalling(item.value, definitions.data.get(header_key))))
        key = f'{parent}.{escape_str(key_cell.value)}' if (parent := definitions.parent) else escape_str(key_cell.value)

        if not any([item[1] for item in items[val_col:]]):
            yield key, None
            if key_cell.value == definitions.endkeyif:
                break
            continue
        for k, v in items:
            if k and v is not FormatType.PASS:
                yield f'{key}.{escape_str(k)}', v

        if key_cell.value == definitions.endkeyif:
            break
