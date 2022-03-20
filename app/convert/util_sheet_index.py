from typing import Tuple, Union

from openpyxl.utils import column_index_from_string


def to_columns_indexes_tuple(columns: str) -> Tuple[int, int]:
    begin, end = columns.split(':', 1)
    return column_index_from_string(begin), column_index_from_string(end)


def to_relative_column_index(column: Union[int, str], base_column: int) -> int:
    return column if isinstance(column, int) else base_column - column_index_from_string(column)
