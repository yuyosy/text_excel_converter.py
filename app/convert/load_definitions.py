
import json
from dacite.core import from_dict

from .definitions_class import DefinisionsFileInfo, DefinitionsData


def load_definisions(info: DefinisionsFileInfo) -> DefinitionsData:
    with info.filename.open('r', encoding=info.encoding) as f:
        data = json.load(f)
    return from_dict(data_class=DefinitionsData, data=data)
