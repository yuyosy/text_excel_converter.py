from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

from dataobject.data_object import DataObject

from .class_definitions import Definitions
from .class_metadata import Metadata

DATETIME_FORMAT = '%Y%m%d-%H%M%S'

def set_metadata(definitions: Definitions, data:DataObject) -> Metadata:
    metadata = Metadata()
    
    return metadata

def get_metadata():
    pass