
from typing import Any, Generator, Tuple

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from .util_convert import get_key_list
from .definitions_class import Definitions
from .escape_str import escape_str
from .marshal_data_format import FormatType, marshalling
from .util_sheet_index import (to_columns_indexes_tuple,
                               to_relative_column_index)


def read_table(workbook: Workbook, definitions: Definitions) -> Generator[Tuple[str, Any], None, None]:
    key = 'aaaaa'
    value = 'aaaaa'
    yield (f'{parent}.{escape_str(key)}' if (parent := definitions.parent) else escape_str(key), value)
