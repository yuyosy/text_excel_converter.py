#
# mdomke/python-ulid
#     https://github.com/mdomke/python-ulid
#     python-ulid/ulid/__init__.py
#
# MIT License
#     Copyright (c) 2017 Martin Domke
#     https://github.com/mdomke/python-ulid/blob/master/LICENSE
#

import os
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Sequence, Union

from .base32 import decode, encode
from .constants import (BYTES_LEN, MILLISECS_IN_SECS, RANDOMNESS_LEN,
                        TIMESTAMP_LEN)


class ULID:

    def __init__(self, value: Optional[bytes] = None) -> None:
        if value is not None and len(value) != BYTES_LEN:
            raise ValueError("ULID has to be exactly 16 bytes long.")
        self.bytes = value or ULID.from_timestamp(time.time()).bytes

    @classmethod
    def from_datetime(cls, value: datetime) -> 'ULID':
        return cls.from_timestamp(value.timestamp())

    @classmethod
    def from_timestamp(cls, value: Union[int, float]) -> 'ULID':
        if isinstance(value, float):
            value = int(value * MILLISECS_IN_SECS)
        timestamp = int.to_bytes(value, TIMESTAMP_LEN, "big")
        randomness = os.urandom(RANDOMNESS_LEN)
        return cls.from_bytes(timestamp + randomness)

    @classmethod
    def from_uuid(cls, value: uuid.UUID) -> 'ULID':
        return cls(value.bytes)

    @classmethod
    def from_uuid_str(cls, value: str) -> 'ULID':
        return cls(uuid.UUID(value).bytes)

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> 'ULID':
        """Create a new :class:`ULID`-object from sequence of 16 bytes."""
        return cls(bytes_)

    @classmethod
    def from_str(cls, string: str) -> 'ULID':
        """Create a new :class:`ULID`-object from a 26 char long string representation."""
        return cls(decode(string))

    @property
    def milliseconds(self) -> int:
        """The timestamp part as epoch time in milliseconds.
        """
        return int.from_bytes(self.bytes[: TIMESTAMP_LEN], byteorder="big")

    @property
    def timestamp(self) -> float:
        """The timestamp part as epoch time in seconds.
        """
        return self.milliseconds / MILLISECS_IN_SECS

    @property
    def datetime(self) -> datetime:
        """Return the timestamp part as timezone-aware :class:`datetime` in UTC.
        """
        return datetime.fromtimestamp(self.timestamp, timezone.utc)

    @property
    def hex(self) -> str:
        """Encode the :class:`ULID`-object as a 32 char sequence of hex values."""
        return self.bytes.hex()

    def to_uuid(self) -> uuid.UUID:
        """Convert the :class:`ULID` to a :class:`uuid.UUID`."""
        return uuid.UUID(bytes=self.bytes)

    def to_uuid_str(self) -> str:
        """Convert the :class:`ULID` to a :class:`uuid.UUID`."""
        return str(uuid.UUID(bytes=self.bytes))

    def __repr__(self) -> str:
        return f"ULID({self!s})"

    def __str__(self) -> str:
        """Encode this object as a 26 character string sequence."""
        return encode(self.bytes)

    def __int__(self) -> int:
        """Encode this object as an integer."""
        return int.from_bytes(self.bytes, byteorder="big")

    def __lt__(self, other) -> bool:
        if isinstance(other, ULID):
            return self.bytes < other.bytes
        elif isinstance(other, int):
            return int(self) < other
        elif isinstance(other, bytes):
            return self.bytes < other
        elif isinstance(other, str):
            return str(self) < other
        return NotImplemented

    def __eq__(self, other) -> bool:
        if isinstance(other, ULID):
            return self.bytes == other.bytes
        elif isinstance(other, int):
            return int(self) == other
        elif isinstance(other, bytes):
            return self.bytes == other
        elif isinstance(other, str):
            return str(self) == other
        return NotImplemented
