from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dataobject.data_object import DataObject
from ulid.ulid import ULID
from util.version_value import VersionValue

from .class_definitions import DefinitionsData
from .class_metadata import Metadata
from .get_hash import get_json_hash


def set_metadata(data: DataObject, definitions_data: DefinitionsData, filename:Path, mode:str) -> None:
    metadata = Metadata()
    now = datetime.now()
    metadata.data_id = str(id) if (id := data.get('$metadata.data_id')) else str(uuid4())
    metadata.chronological_id_current = ULID()
    metadata.chronological_id_previous = ULID.from_uuid_str(id) if (id := data.get('$metadata.chronological_id_current')) else None

    metadata.datetime_created = dt if isinstance(dt := data.get('$metadata.datetime_created'), datetime) else now
    metadata.datetime_modified = dt if isinstance(dt := data.get('$metadata.datetime_modified'), datetime) else now
    metadata.datetime_generated_excel = dt if isinstance(dt := data.get('$metadata.datetime_generated_excel'), datetime) else None
    metadata.datetime_generated_text = dt if isinstance(dt := data.get('$metadata.datetime_generated_text'), datetime) else None
    if mode == 'excel':
        metadata.datetime_generated_excel = now
    elif mode == 'text':
        metadata.datetime_generated_text = now

    metadata.name = definitions_data.name
    metadata.format_version = VersionValue(definitions_data.format_version)
    metadata.definitions_file = definitions_data.file_name
    metadata.source_data = filename
    metadata.data_version = VersionValue(str(ver)) if (ver := data.get('$metadata.data_version')) else VersionValue('0')
    attrdict = data.asattrdict()
    attrdict.pop('$metadata', None)
    metadata.data_hash_current = get_json_hash(attrdict)
    metadata.data_hash_previous = str(hs) if (hs := data.get('$metadata.data_hash_current')) else None
    if metadata.data_hash_current != metadata.data_hash_previous:
        metadata.datetime_modified = now
        metadata.data_version.increment('1')


    data.update({'$metadata': metadata.todict()})