
from distutils.version import LooseVersion
from typing import Callable, List, Union


class VersionValue(LooseVersion):
    def increment(self, ver: str) -> None:
        self._assign(ver, self._add)

    def decrement(self, ver: str) -> None:
        self._assign(ver, self._sub)

    def _add(self, a: int, b: int) -> int:
        return a + b

    def _sub(self, a: int, b: int) -> int:
        return a - b

    def _assign(self, ver: str, func: Callable[[int, int], int]) -> None:
        vstr = [str(x) for x in self.component_re.split(ver) if x and x != '.']
        cm: List[Union[str, int]] = [0] * (n if (n := len(self.version) - len(vstr)) > 0 else 0)
        cm.extend(vstr)

        for i, item in enumerate(self.version):
            if isinstance(item, str):
                if len(item) == 1:
                    vi = func(ord(item), int(cm[i]))
                    if vi > 122:
                        cm[i] = 'z'+chr(vi-26)
                    else:
                        cm[i] = chr(vi)
                else:
                    cm[i] = item[:-1] + chr(func(ord(item[-1]), int(cm[i])))
            else:
                cm[i] = func(item, int(cm[i]))
        self.version = tuple(cm)
        self.vstring = '.'.join(map(str, cm))

    def __repr__(self) -> str:
        return f"VersionValue('{str(self)}')"

    def __str__(self) -> str:
        return self.vstring
