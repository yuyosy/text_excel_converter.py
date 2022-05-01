# 
# This code inspired by works distributed under Copyright (c) 2014 Carlos Escribano Rey (MIT License).
# 
# inspired by carlosescri's DottedDict Library.
# 
# carlosescri/DottedDict
#     https://github.com/carlosescri/DottedDict
# 

import re
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping, MutableSequence
from typing import Any, Dict, Iterator, List, Tuple, Union

SEPARATOR_REGEX = r'(?<!\\)(\.)'


def is_dotted_key(key: str) -> bool:
    return len(re.findall(SEPARATOR_REGEX, key)) > 0


def split_key_string(key: str, max_keys: int = 0) -> List[str]:
    parts = [x for x in re.split(SEPARATOR_REGEX, key) if x != "."]
    result = []
    while len(parts) > 0:
        if max_keys > 0 and len(result) == max_keys:
            break
        result.append(parts.pop(0))

    if len(parts) > 0:
        result.append(".".join(parts))
    return result


def make(initial: Union[Dict[str, Any], List[Any], None] = None) -> Any:
    if isinstance(initial, list):
        return DottedList(initial)
    elif isinstance(initial, dict):
        return DottedDict(initial)
    else:
        return initial


def make_by_index(dotted_key: str) -> Any:
    if not isinstance(dotted_key, str):
        next_key = str(dotted_key)
    elif not is_dotted_key(dotted_key):
        next_key = dotted_key
    else:
        next_key, _ = split_key_string(dotted_key, 1)

    return make([] if isinstance(next_key, int) else {})


class DataObject():

    def __init__(self, initial: Union[Dict[str, Any], List[Any]] = {}) -> None:
        self.data: BaseDataObject = DottedDict({}) if (d := make(initial)) is None else d

    # Public Instance Methods
    def get(self, key: Union[str, int], default: Any = None) -> Union['BaseDataObject', Any]:
        try:
            return self.data.__getitem__(key)  # type: ignore
        except KeyError:
            return default

    def set(self, key: Union[str, int], value: Any) -> None:
        self.data.__setitem__(key, value)  # type: ignore

    def update(self, value: Dict[str, Any]) -> None:
        if isinstance(self.data, DottedDict) and isinstance(value, dict):
            data = iter(value.items())
            for key, value in data:
                self.data[key] = make(value)

    def insert(self, index, value: Any) -> None:
        if isinstance(self.data, DottedList):
            return self.data.insert(index, value)

    def pop(self, key: Union[str, int], value: Any = None) -> Union['BaseDataObject', Any]:
        try:
            value = self[key]
            del self[key]
        except KeyError:
            if value is None:
                raise
        return value

    def to_plain(self) -> Any:
        return self.data.to_plain()

    # Magic Methods

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self.data)

    def __repr__(self) -> str:
        return repr(self.data)

    def __getitem__(self, key: Union[str, int]) -> Union['BaseDataObject', Any]:
        return self.data.__getitem__(key)  # type: ignore

    def __setitem__(self, key: Union[str, int], value: Any) -> None:
        return self.data.__setitem__(key, value)  # type: ignore

    def __delitem__(self, key: Union[str, int]) -> None:
        return self.data.__delitem__(key)  # type: ignore


class BaseDataObject(object, metaclass=ABCMeta):

    def __init__(self, initial):
        if not isinstance(initial, list) and not isinstance(initial, dict):
            raise ValueError('initial value must be list or dict')

        self._validate_initial_value(initial)

        self._data = initial

        if isinstance(initial, list):
            data = enumerate(initial)
        else:
            data = iter(initial.items())

        for key, value in data:
            try:
                self._data[key] = make(value)
            except ValueError:
                pass

    def _validate_initial_value(self, initial: Union[Dict[str, Any], List[Any], None]) -> None:
        if isinstance(initial, list):
            for item in initial:
                self._validate_initial_value(item)
        elif isinstance(initial, dict):
            for key, item in iter(initial.items()):
                if is_dotted_key(key):
                    raise ValueError(f'{key} is not a valid key')
                self._validate_initial_value(item)

    @abstractmethod
    def to_plain(self) -> Any:
        pass

    # Magic Methods

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    @abstractmethod
    def __getitem__(self, key: Union[str, int]) -> Union['BaseDataObject', Any]:
        pass

    @abstractmethod
    def __setitem__(self, key: Union[str, int], value: Any) -> None:
        pass

    @abstractmethod
    def __delitem__(self, key: Union[str, int]) -> None:
        pass


class DottedList(BaseDataObject, MutableSequence):

    def __init__(self, initial: Union[Dict[str, Any], List[Any], None] = None):
        self._data: List
        BaseDataObject.__init__(self, [] if initial is None else list(initial))

    def insert(self, index, value):
        self._data.insert(index, value)

    def to_plain(self) -> Any:
        result = list(self)
        for index, value in enumerate(result):
            if isinstance(value, BaseDataObject):
                result[index] = value.to_plain()
        return result

    # Magic Methods

    def __getitem__(self, index: Union[str, int]) -> Union[BaseDataObject, Any]:
        if isinstance(index, slice):
            return self._data[index]

        if isinstance(index, int) or (isinstance(index, str) and index.isdigit()):
            print(int(index))
            return self._data[int(index)]

        elif isinstance(index, str) and is_dotted_key(index):
            my_index, alt_index = split_key_string(index, 1)
            target = self._data[int(my_index)]

            if not isinstance(target, BaseDataObject):
                raise IndexError(f'cannot get "{alt_index}" in "{my_index}" ({repr(target)})')
            return target[alt_index]

        else:
            raise IndexError('cannot get %s in %s' % (index, repr(self._data)))

    def __setitem__(self, index: Union[str, int], value: Any) -> None:
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit()):
            if int(index) not in self._data and int(index) == len(self._data):
                self._data.append(make(value))
            else:
                self._data[int(index)] = make(value)

        elif isinstance(index, str) and is_dotted_key(index):
            my_index, alt_index = split_key_string(index, 1)

            if int(my_index) not in self._data and int(my_index) == len(self._data):
                self._data.append(make_by_index(alt_index))

            if not isinstance(self[int(my_index)], BaseDataObject):
                raise IndexError(f'cannot set {alt_index} in {my_index} ({repr(self[int(my_index)])})')

            self._data[int(my_index)][alt_index] = make(value)

        else:
            raise IndexError(f'cannot use {index} as index in {repr(self._data)}')

    def __delitem__(self, index: Union[str, int]):
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit()):
            del self._data[int(index)]

        elif isinstance(index, str) and is_dotted_key(index):
            my_index, alt_index = split_key_string(index, 1)
            target = self._data[int(my_index)]

            if not isinstance(target, BaseDataObject):
                raise IndexError(f'cannot delete {alt_index} in {my_index} ({repr(target)})')

            del target[alt_index]

        else:
            raise IndexError(f'cannot delete {index} in {repr(self._data)}')


class DottedDict(BaseDataObject, MutableMapping):

    def __init__(self, initial: Union[Dict[str, Any], List[Any], None] = None):
        self._data: Dict[str, Any]
        BaseDataObject.__init__(self, {} if initial is None else dict(initial))

    def update(self, data: Dict[str, Any]) -> None:
        self._data.update(data)

    def to_plain(self):
        result = dict(self)

        for key, value in iter(result.items()):
            if isinstance(value, BaseDataObject):
                result[key] = value.to_plain()

        return result

    # Magic Methods

    def __getitem__(self, k: str) -> Union[BaseDataObject, Any]:
        key = self.__keytransform__(k)

        if not isinstance(k, str) or not is_dotted_key(key):

            try:
                return self._data[key]
            except KeyError as e:
                raise KeyError(e)

        my_key, alt_key = split_key_string(key, 1)
        target = self._data[my_key]

        if not isinstance(target, BaseDataObject):
            raise KeyError(f'cannot get  {alt_key} in {my_key} ({repr(target)})')

        return target[alt_key]

    def __setitem__(self, k: str, value: Any) -> None:
        key = self.__keytransform__(k)

        if not isinstance(k, str):
            raise KeyError('keys must be str')
        elif not is_dotted_key(key):
            self._data[key] = make(value)
        else:
            my_key, alt_key = split_key_string(key, 1)

            if my_key not in self._data:
                self._data[my_key] = make_by_index(alt_key)

            if self._data[my_key] is None:
                self._data[my_key] = DottedDict()
            self._data[my_key][alt_key] = value

    def __delitem__(self, k: str) -> None:
        key = self.__keytransform__(k)

        if not isinstance(k, str) or not is_dotted_key(key):
            del self._data[key]

        else:
            my_key, alt_key = split_key_string(key, 1)
            target = self._data[my_key]

            if not isinstance(target, BaseDataObject):
                raise KeyError(f'cannot delete "{alt_key}" in "{my_key}" ({repr(target)})')

            del target[alt_key]

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.__dict__ or key == '_data':
            object.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)

    def __delattr__(self, key: str) -> None:
        if key in self.__dict__ or key == '_data':
            object.__delattr__(self, key)
        else:
            self.__delitem__(key)

    def __contains__(self, k: str) -> bool:
        key = self.__keytransform__(k)

        if not isinstance(k, str) or not is_dotted_key(key):
            return self._data.__contains__(key)

        my_key, alt_key = split_key_string(key, 1)
        if not self._data.__contains__(my_key):
            return False
        target: Dict[str, Any] = self._data[my_key]

        if not isinstance(target, BaseDataObject):
            return False

        return alt_key in target

    def __keytransform__(self, key: str) -> str:
        return key

    __getattr__ = __getitem__
