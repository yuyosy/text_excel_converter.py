
from typing import Any, Iterator, Tuple

from dataobject.data_object import DataObject
from openpyxl.cell import Cell
from openpyxl.workbook.workbook import Workbook

from .class_definitions import Definitions
from .escape_str import escape_str
from .marshal_data_format import FormatType, unmarshalling
from .util_convert import get_key_list
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def write_keyvalue(workbook: Workbook, data: DataObject, definitions: Definitions) -> Iterator[Tuple[Cell, Any]]:
    sheet = workbook[definitions.sheet]
    key_list = get_key_list(definitions.data)

    min_col, max_col = to_columns_indexes_tuple(definitions.columns)
    key_col = to_relative_column_index(0 if (c := definitions.key_col) is None else c, min_col)
    val_col = to_relative_column_index(0 if (c := definitions.value_col) is None else c, min_col)
    header_row = 0 if (c := definitions.header_row) is None else c
    begin_row = 0 if (c := definitions.begin_row) is None else c

    for row in sheet.iter_rows(min_row=begin_row, min_col=min_col, max_col=max_col):
        key_cell = row[key_col]
        val_cell = row[val_col]
        if key_cell.value is None:
            break
        key = key_list.get(key_cell.value, None)
        if key is None:
            continue
        k = f'{parent}.{escape_str(key)}' if (parent := definitions.parent) else escape_str(key)
        value = unmarshalling(data.get(k, None), definitions.data.get(key))
        if value is FormatType.PASS:
            continue
        # val_cell.value = value
        yield val_cell, value
        if key_cell.value == definitions.endkeyif:
            break
