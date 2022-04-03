
import json
from dacite.core import from_dict

from .class_definitions import DefinisionsFileInfo, DefinitionsData


def load_definisions(info: DefinisionsFileInfo) -> DefinitionsData:
    with info.filename.open('r', encoding=info.encoding) as f:
        data = json.load(f)
    dfsdata = from_dict(data_class=DefinitionsData, data=data)
    dfsdata.file_name = info.filename
    return dfsdata
