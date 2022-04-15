from abc import abstractmethod
from dataclasses import asdict, dataclass

from config.config_class import ConfigApp
from dataobject.data_object import DataObject

from .class_definitions import DefinitionsData
from .class_metadata import Metadata


@dataclass
class Converter():
    config: ConfigApp
    data: DataObject
    definition_data: DefinitionsData
    metadata: Metadata

    def __init__(self, config: ConfigApp) -> None:
        self.config = config
        self.data = DataObject()
        self.data.update({'$metadata': Metadata().todict()})

    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def write(self) -> None:
        pass
