from dataclasses import dataclass
from distutils.version import StrictVersion
from pathlib import Path
from typing import Any, Dict, List, Optional, Union



@dataclass
class CellInfo():
    sheet: str
    cell: str


@dataclass
class DefinisionsFileInfo():
    name: str
    version: StrictVersion
    compatibility: StrictVersion
    filename: Path
    version_def: CellInfo
    encoding: str
    update_date: Optional[str]


@dataclass
class Definitions:
    # Required
    type: str
    sheet: str
    columns: str
    data: Dict[str, Any]
    # Optional
    header_row: Optional[int]
    begin_row: Optional[int]
    key_col: Optional[Union[int, str]]
    value_col: Optional[Union[int, str]]
    endkeyif: Optional[Union[int, str]]
    overwrite_keycol: Optional[bool]
    parent: Optional[str]


@dataclass
class DefinitionsData():
    # Required
    name: str
    format_version: str
    format_definition_cell: CellInfo
    includes: List[str]
    definitions: Dict[str, Definitions]
    # Optional
    schema_version: Optional[str]
    description: Optional[str]
    date_created: Optional[str]
    date_updated: Optional[str]
    template_name: Optional[str]
    file_datetime_format: Optional[str]
    output_filename: Optional[str]
    excludes: Optional[List[str]]
