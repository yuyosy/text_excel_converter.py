import re
from typing import (Any, Dict, List, Generator, ItemsView, Iterator, KeysView,
                    Mapping, Tuple, Union, ValuesView, cast)


class AttributeDataObject(Dict[str, Any]):
    def __getattr__(self, key: Any) -> Any:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: Any, value: Any) -> None:
        self[key] = value


class DataObject:
    def __init__(self, data: Dict[str, Any] = {}, *,
                 lowercase: bool = False,
                 separator_escape: str = r'(?<!\\)\.'
                 ) -> None:
        self.lowercase = lowercase
        self.separator_escape = separator_escape
        self._dotted_dict: Dict[str, Any] = self._flatten(data)

    # Property

    @property
    def lowercase(self):
        return self.__lowercase

    @lowercase.setter
    def lowercase(self, lowercase: bool):
        if type(lowercase) != bool:
            raise TypeError('lowercase invalid type')
        self.__lowercase = lowercase

    @property
    def separator_escape(self):
        return self.__separator_escape.pattern

    @separator_escape.setter
    def separator_escape(self, separator_escape: str):
        self.__separator_escape = re.compile(separator_escape)

    # Public Instance Methods
    # Like the built-in dict type.

    def set(self, key: str, value: Any = None) -> None:
        self._dotted_dict[key] = value

    def get(self, key: str, default: Any = None) -> Union[Dict[str, Any], Any]:
        return self._dotted_dict.get(key, default)

    def update(self, data: Dict[str, Any]) -> None:
        self._dotted_dict.update(self._flatten(data))

    def setdefault(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            self[key] = default
        return self[key]

    def copy(self) -> 'DataObject':
        return DataObject(self._dotted_dict)

    def pop(self, key: str, value: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
        except KeyError:
            if value is None:
                raise
        return value

    def catchup(self, key: str) -> Union['DataObject', Any]:
        d = self._get_children(key)
        return DataObject(d) if isinstance(d, (dict, DataObject)) else d

    def keys(self) -> Union['DataObject', Any, KeysView[str]]:
        try:
            return self['keys']
        except KeyError:
            return cast(KeysView[str], list({'.'.join(re.split(self.separator_escape, k)[:1]) for k in set(self.asdict().keys())}))

    def values(self) -> Union['DataObject', Any, ValuesView[Any]]:
        try:
            return self['values']
        except KeyError:
            return dict(self.items()).values()

    def items(self) -> Union['DataObject', ItemsView[str, Any]]:
        try:
            return self['items']
        except KeyError:
            keys = cast(KeysView[str], self.keys())
            return {k: self._get_children(k) for k in keys}.items()

    def asdict(self) -> Dict[str, Any]:
        return self._dotted_dict

    def asattrdict(self) -> AttributeDataObject:
        return AttributeDataObject(self._unflatten())

    # Internal Instance Methods

    def _flatten_items(self, flat_dict: Dict[str, Any], data: Dict[str, Any], *, depth: int, parent: str = '') -> bool:
        has_item = False
        for key, value in data.items():
            has_item = True
            if not parent:
                flat_key = key
            else:
                flat_key = f'{parent}.{key}'
            if isinstance(value, Dict):
                has_child = self._flatten_items(flat_dict, value, depth=depth + 1, parent=flat_key)
                if has_child or not isinstance(value, tuple):
                    continue
            if flat_key in flat_dict.keys():
                raise ValueError(f'duplicated key {flat_key}')
            flat_dict[flat_key] = value
        return has_item

    def _flatten(self, data: Dict[str, Any]) -> Dict[str, Any]:
        flat_dict: Dict[str, Any] = {}
        self._flatten_items(flat_dict, data, depth=1)
        return flat_dict

    def _unflattern_items(self, data: Dict[str, Any], keys: List[str], value: Any) -> None:
        assert keys
        if data is None:
            return
        key = keys[0]
        if len(keys) == 1:
            if key in data:
                raise ValueError(f'duplicated key {key}')
            data[key] = value
            return
        data = data.setdefault(key, {})
        self._unflattern_items(data, keys[1:], value)

    def _unflatten(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for flat_key, value in self._dotted_dict.items():
            key_tuple = re.split(self.separator_escape, flat_key)
            self._unflattern_items(data, key_tuple, value)
        return data

    def _iter_item(self, data: Mapping[str, Any], key: str) -> Generator[Tuple[str, Any], None, None]:
        for k, v in data.items():
            if k.startswith(key + '.'):
                yield k, v

    def _get_items(self, data: Dict[str, Any], key: str) -> Dict[str, Any]:
        if self.lowercase:
            return {k[(len(key) + 1):].lower(): v for k, v in data.items() for k, v in self._iter_item(data, key)}
        else:
            return {k[(len(key) + 1):]: v for k, v in self._iter_item(data, key)}

    def _get_children(self, key: str) -> Union[Dict[str, Any], Any]:
        data = {k[(len(key) + 1):]: v for k, v in self._iter_item(self._dotted_dict, key)}
        if not data:
            attributes = re.split(self.separator_escape, key)
            if len(attributes) == 1:
                return self._dotted_dict.get(key, {})
            data = self._dotted_dict
            while attributes:
                p = attributes[0]
                d = self._get_items(data, p)
                if d == {}:
                    return data.get(p, {}) if len(attributes) == 1 else {}
                data = d
                attributes = attributes[1:]
        return data

    # Magic Methods
    # Like the built-in dict type.

    def __len__(self) -> int:
        return len(self.keys())

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __getitem__(self, item: str) -> Union['DataObject', Any]:
        v = self._get_children(item)
        if v == {}:
            raise KeyError(f'"{item}" key not found')
        if isinstance(v, dict):
            return DataObject(v)
        else:
            return v

    def __setitem__(self, key: str, value: Any) -> None:
        self.update({key: value})

    def __delitem__(self, key: str) -> None:
        remove: List[str] = []
        for k in self._dotted_dict:
            kl = k.lower() if self.lowercase else k
            if kl == key or kl.startswith(key + '.'):
                remove.append(k)
        if not remove:
            raise KeyError(f'"{key}" key not found')
        for k in remove:
            del self._dotted_dict[k]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self.items())

    def __reversed__(self) -> Iterator[Tuple[str, Any]]:
        return iter(reversed(self.items()))

    def __contains__(self, key: str) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __eq__(self, other: Any) -> bool:
        return self.asdict() == DataObject(other).asdict()

    def __repr__(self) -> str:
        return f'<DataObject: {hex(id(self))}>'

    def __str__(self) -> str:
        return str({k: v for k, v in sorted(self.asdict().items())})
