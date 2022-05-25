# Experimental Feature

from typing import Any, Iterator, List, Tuple

from dataobject.data_object import DataObject
from openpyxl.cell import Cell
from openpyxl.workbook.workbook import Workbook

from .class_definitions import Definitions
from .escape_str import escape_str, unescape_str
from .marshal_data_format import FormatType, unmarshalling
from .util_convert import get_key_list
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def write_matrix(workbook: Workbook, data: DataObject, definitions: Definitions) -> Iterator[Tuple[Cell, Any]]:
    sheet = workbook[definitions.sheet]
    key_list = get_key_list(definitions.data)

    min_col, max_col = to_columns_indexes_tuple(definitions.columns)
    matrix_parent_col = to_relative_column_index(0 if (c := definitions.matrix_parent_col) is None else c, min_col)
    key_col = to_relative_column_index(0 if (c := definitions.key_col) is None else c, min_col)
    val_col = to_relative_column_index(0 if (c := definitions.value_col) is None else c, min_col)
    header_row = 0 if (c := definitions.header_row) is None else c
    begin_row = 0 if (c := definitions.begin_row) is None else c

    header = [col.value for col in sheet[header_row][min_col-1:max_col]]
    # t_data = data.to_plain()
    if not definitions.parent:
        return
    dv = definitions.parent.split('.${matrix_parent_key}')
    data_group:Any = data.get(dv[0].rstrip('.'))
    table_data = []
    for key, item in data_group.items():
        children = item
        if dv[1]:
            children = item.get(dv[1].lstrip('.'))
        for ch in children.values():
            table_data.append([key, ch])
    max_row = begin_row+len(table_data)

    # keys_list = table_data[0][1].keys()
    for data_item, row in zip(iter(table_data), sheet.iter_rows(min_row=begin_row, max_row=max_row, min_col=min_col, max_col=max_col)):
        matrix_parent_cell = row[matrix_parent_col]
        key_cell = row[key_col]
        # if not key_cell.value:
        #     continue
        # d = table_data[1].get(escape_str(data_key)) or {}
        d = data_item[1]
        cells_data: List[Tuple[Cell, Any]] = [(matrix_parent_cell, data_item[0])]
        key_header_value = key_list.get(header[key_col], None)
        for head, cell in zip(header, row):
            header_key = key_list.get(head, '')
            if not header_key:
                continue
            if definitions.overwrite_keycol and header_key == key_header_value:
                cells_data.append((cell, unmarshalling(unescape_str(d.get(header_key)), definitions.data.get(header_key))))
            else:
                cells_data.append((cell, unmarshalling(d.get(header_key), definitions.data.get(header_key))))
                
        # if key_cell.value == definitions.endkeyif:
        #     break

        for k, v in cells_data:
            if k and v is not FormatType.PASS:
                # k.value = v
                yield k, v
        if key_cell.value == definitions.endkeyif:
            break
