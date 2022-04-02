from dataclasses import dataclass
from datetime import datetime
from distutils.version import StrictVersion
from pathlib import Path
from typing import Optional
from uuid import UUID

from ulid.ulid import ULID
from util.version_value import VersionValue


@dataclass
class Metadata():
    data_id: Optional[UUID] = None
    chronological_id: Optional[ULID] = None
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
