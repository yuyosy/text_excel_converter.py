from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ulid.ulid import ULID
from util.version_value import VersionValue

from .const import DATETIME_FORMAT


@dataclass
class Metadata():
    data_id: Optional[str] = None
    chronological_id_current: Optional[ULID] = None
    chronological_id_previous: Optional[ULID] = None
    name: Optional[str] = None
    format_version: Optional[VersionValue] = None
    definitions_file: Optional[Path] = None
    source_data: Optional[Path] = None
    datetime_created: Optional[datetime] = None
    datetime_modified: Optional[datetime] = None
    datetime_generated_excel: Optional[datetime] = None
    datetime_generated_text: Optional[datetime] = None
    data_version: Optional[VersionValue] = None
    data_hash_current: Optional[str] = None
    data_hash_previous: Optional[str] = None

    def todict(self) -> Dict[str, Any]:
        return {
            'data_id': None if self.data_id is None else self.data_id,
            'chronological_id_current': None if self.chronological_id_current is None else self.chronological_id_current.to_uuid_str(),
            'chronological_id_previous': None if self.chronological_id_previous is None else self.chronological_id_previous.to_uuid_str(),
            'name': None if self.name is None else self.name,
            'format_version': None if self.format_version is None else str(self.format_version),
            'definitions_file': None if self.definitions_file is None else self.definitions_file.name,
            'source_data': None if self.source_data is None else self.source_data.name,
            'datetime_created': None if self.datetime_created is None else self.datetime_created.strftime(DATETIME_FORMAT),
            'datetime_modified': None if self.datetime_modified is None else self.datetime_modified.strftime(DATETIME_FORMAT),
            'datetime_generated_excel': None if self.datetime_generated_excel is None else self.datetime_generated_excel.strftime(DATETIME_FORMAT),
            'datetime_generated_text': None if self.datetime_generated_text is None else self.datetime_generated_text.strftime(DATETIME_FORMAT),
            'data_version': None if self.data_version is None else str(self.data_version),
            'data_hash_current': None if self.data_hash_current is None else self.data_hash_current,
            'data_hash_previous': None if self.data_hash_previous is None else self.data_hash_previous,
        }
