from abc import abstractmethod
from dataclasses import dataclass

from config.config_class import ConfigApp
from dataobject.data_object import DataObject

from .definitions_class import DefinitionsData


@dataclass
class Converter():
    config: ConfigApp
    data: DataObject
    definition_data: DefinitionsData

    def __init__(self, config: ConfigApp) -> None:
        self.config = config
        self.data = DataObject()

    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def write(self) -> None:
        pass
