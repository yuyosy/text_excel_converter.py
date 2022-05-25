
from typing import Any, Iterator, List, Tuple

from openpyxl.workbook.workbook import Workbook

from .class_definitions import Definitions
from .escape_str import escape_str
from .marshal_data_format import FormatType, marshalling
from .util_convert import get_key_list
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def read_matrix(workbook: Workbook, definitions: Definitions) -> Iterator[Tuple[str, Any]]:
    sheet = workbook[definitions.sheet]
    key_list = get_key_list(definitions.data)

    min_col, max_col = to_columns_indexes_tuple(definitions.columns)
    matrix_parent_col = to_relative_column_index(0 if (c := definitions.matrix_parent_col) is None else c, min_col)
    key_col = to_relative_column_index(0 if (c := definitions.key_col) is None else c, min_col)
    val_col = to_relative_column_index(0 if (c := definitions.value_col) is None else c, min_col)
    header_row = 0 if (c := definitions.header_row) is None else c
    begin_row = 0 if (c := definitions.begin_row) is None else c

    header = [col.value for col in sheet[header_row][min_col-1:max_col]]

    for row in sheet.iter_rows(min_row=begin_row, min_col=min_col, max_col=max_col):
        if not any(cell.value for cell in row):
            break
        matrix_parent_cell = row[matrix_parent_col]
        key_cell = row[key_col]
        if not matrix_parent_cell.value or not key_cell.value:
            continue
        items: List[Tuple[str, Any]] = []
        zipped = list(zip(header, row))
        keycol_head, keycol_cell = zipped.pop(key_col)
        _, matrix_parentcol_cell = zipped.pop(matrix_parent_col)
        keycol_header_key = key_list.get(keycol_head, '')
        keycol_items = marshalling(keycol_cell.value, definitions.data.get(keycol_header_key))
        for head, item in zipped:
            header_key = key_list.get(head, '')
            if not header_key:
                continue
            items.append((header_key, marshalling(item.value, definitions.data.get(header_key))))
        key = f'{parent}.{escape_str(key_cell.value)}' if (parent := definitions.parent) else escape_str(key_cell.value)
        key = key.replace('${matrix_parent_key}', matrix_parentcol_cell.value)
        if not any([item[1] for item in items]):
            yield key, None
            if key_cell.value == definitions.endkeyif:
                break
            continue
        
        if keycol_header_key:
            yield f'{key}.{escape_str(keycol_header_key)}', keycol_items
        for k, v in items:
            if k and v is not FormatType.PASS:
                yield f'{key}.{escape_str(k)}', v

        if key_cell.value == definitions.endkeyif:
            break
