
from typing import Any, Generator, Tuple

from openpyxl.workbook.workbook import Workbook

from .definitions_class import Definitions
from .escape_str import escape_str
from .marshal_data_format import FormatType, marshalling
from .util_convert import get_key_list
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def read_keyvalue(workbook: Workbook, definitions: Definitions) -> Generator[Tuple[str, Any], None, None]:
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
        if key_cell.value is None and val_cell.value is None:
            break
        key = key_list.get(key_cell.value, None)
        if key is None:
            continue
        value = marshalling(val_cell.value, definitions.data.get(key))
        if value is FormatType.PASS:
            continue
        yield (f'{parent}.{escape_str(key)}' if (parent := definitions.parent) else escape_str(key), value)
        if key_cell.value == definitions.endkeyif:
            break
