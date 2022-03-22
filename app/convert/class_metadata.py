
import inspect
from typing import Any, Dict


class Metadata():
    def __init__(self) -> None:
        self._data_id: str = ''
        self.chronological_id: str = ''
        self.name: str = ''
        self.format_version: str = ''
        self.definitions_file: str = ''
        self.source_data: str = ''
        self._datetime_created: str = ''
        self.datetime_modified: str = ''
        self.datetime_generated_excel: str = ''
        self.datetime_generated_text: str = ''
        self.data_version: str = ''
        self.data_hash_current: str = ''
        self.data_hash_previous: str = ''

    @property
    def data_id(self) -> str:
        return self._datetime_created

    @data_id.setter
    def data_id(self, s: str) -> None:
        if not self._data_id:
            self._data_id = s

    @property
    def datetime_created(self) -> str:
        return self._datetime_created

    @datetime_created.setter
    def datetime_created(self, s: str) -> None:
        if not self._datetime_created:
            self._datetime_created = s

    def init_data(self):
        pass

    def asdict(self) -> Dict[str, Any]:
        data = {}
        members = dict(inspect.getmembers(self))
        for key in self.__dict__.keys():
            k = key.strip('_')
            data[k] = members.get(k)
        return data
