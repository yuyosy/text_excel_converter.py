#
# mdomke/python-ulid
#     https://github.com/mdomke/python-ulid
#     python-ulid/ulid/base32.py
#
# MIT License
#     Copyright (c) 2017 Martin Domke
#     https://github.com/mdomke/python-ulid/blob/master/LICENSE
#


from typing import Sequence

from .constants import (BYTES_LEN, RANDOMNESS_LEN, RANDOMNESS_REPR_LEN,
                        REPR_LEN, TIMESTAMP_LEN, TIMESTAMP_REPR_LEN)

ENCODE: str = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
DECODE: Sequence[int] = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x01,
                         0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0xFF, 0xFF,
                         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E,
                         0x0F, 0x10, 0x11, 0xFF, 0x12, 0x13, 0xFF, 0x14, 0x15, 0xFF,
                         0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C, 0x1D, 0x1E,
                         0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0A, 0x0B, 0x0C,
                         0x0D, 0x0E, 0x0F, 0x10, 0x11, 0xFF, 0x12, 0x13, 0xFF, 0x14,
                         0x15, 0xFF, 0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C,
                         0x1D, 0x1E, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, ]


def encode(binary: bytes) -> str:
    if len(binary) != BYTES_LEN:
        raise ValueError("ULID has to be exactly 16 bytes long")
    return encode_timestamp(binary[: TIMESTAMP_LEN]) + encode_randomness(
        binary[TIMESTAMP_LEN:]
    )


def encode_timestamp(binary: bytes) -> str:
    if len(binary) != TIMESTAMP_LEN:
        raise ValueError("Timestamp value has to be exactly 6 bytes long.")
    lut = ENCODE
    return "".join(
        [
            lut[(binary[0] & 224) >> 5],
            lut[(binary[0] & 31)],
            lut[(binary[1] & 248) >> 3],
            lut[((binary[1] & 7) << 2) | ((binary[2] & 192) >> 6)],
            lut[((binary[2] & 62) >> 1)],
            lut[((binary[2] & 1) << 4) | ((binary[3] & 240) >> 4)],
            lut[((binary[3] & 15) << 1) | ((binary[4] & 128) >> 7)],
            lut[(binary[4] & 124) >> 2],
            lut[((binary[4] & 3) << 3) | ((binary[5] & 224) >> 5)],
            lut[(binary[5] & 31)],
        ]
    )


def encode_randomness(binary: bytes) -> str:
    if len(binary) != RANDOMNESS_LEN:
        raise ValueError("Randomness value has to be exactly 10 bytes long.")
    lut = ENCODE
    return "".join(
        [
            lut[(binary[0] & 248) >> 3],
            lut[((binary[0] & 7) << 2) | ((binary[1] & 192) >> 6)],
            lut[(binary[1] & 62) >> 1],
            lut[((binary[1] & 1) << 4) | ((binary[2] & 240) >> 4)],
            lut[((binary[2] & 15) << 1) | ((binary[3] & 128) >> 7)],
            lut[(binary[3] & 124) >> 2],
            lut[((binary[3] & 3) << 3) | ((binary[4] & 224) >> 5)],
            lut[(binary[4] & 31)],
            lut[(binary[5] & 248) >> 3],
            lut[((binary[5] & 7) << 2) | ((binary[6] & 192) >> 6)],
            lut[(binary[6] & 62) >> 1],
            lut[((binary[6] & 1) << 4) | ((binary[7] & 240) >> 4)],
            lut[((binary[7] & 15) << 1) | ((binary[8] & 128) >> 7)],
            lut[(binary[8] & 124) >> 2],
            lut[((binary[8] & 3) << 3) | ((binary[9] & 224) >> 5)],
            lut[(binary[9] & 31)],
        ]
    )


def decode(encoded: str) -> bytes:
    if len(encoded) != REPR_LEN:
        raise ValueError("Encoded ULID has to be exactly 26 characters long.")
    return decode_timestamp(encoded[: TIMESTAMP_REPR_LEN]) + decode_randomness(
        encoded[TIMESTAMP_REPR_LEN:]
    )


def decode_timestamp(encoded: str) -> bytes:
    if len(encoded) != TIMESTAMP_REPR_LEN:
        raise ValueError("ULID timestamp has to be exactly 10 characters long.")
    lut = DECODE
    values: bytes = bytes(encoded, "ascii")
    return bytes(
        [
            ((lut[values[0]] << 5) | lut[values[1]]) & 0xFF,
            ((lut[values[2]] << 3) | (lut[values[3]] >> 2)) & 0xFF,
            ((lut[values[3]] << 6) | (lut[values[4]] << 1) | (lut[values[5]] >> 4)) & 0xFF,
            ((lut[values[5]] << 4) | (lut[values[6]] >> 1)) & 0xFF,
            ((lut[values[6]] << 7) | (lut[values[7]] << 2) | (lut[values[8]] >> 3)) & 0xFF,
            ((lut[values[8]] << 5) | (lut[values[9]])) & 0xFF,
        ]
    )


def decode_randomness(encoded: str) -> bytes:
    if len(encoded) != RANDOMNESS_REPR_LEN:
        raise ValueError("ULID randomness has to be exactly 16 characters long.")
    lut = DECODE
    values = bytes(encoded, "ascii")
    return bytes(
        [
            ((lut[values[0]] << 3) | (lut[values[1]] >> 2)) & 0xFF,
            ((lut[values[1]] << 6) | (lut[values[2]] << 1) | (lut[values[3]] >> 4)) & 0xFF,
            ((lut[values[3]] << 4) | (lut[values[4]] >> 1)) & 0xFF,
            ((lut[values[4]] << 7) | (lut[values[5]] << 2) | (lut[values[6]] >> 3)) & 0xFF,
            ((lut[values[6]] << 5) | (lut[values[7]])) & 0xFF,
            ((lut[values[8]] << 3) | (lut[values[9]] >> 2)) & 0xFF,
            ((lut[values[9]] << 6) | (lut[values[10]] << 1) | (lut[values[11]] >> 4)) & 0xFF,
            ((lut[values[11]] << 4) | (lut[values[12]] >> 1)) & 0xFF,
            ((lut[values[12]] << 7) | (lut[values[13]] << 2) | (lut[values[14]] >> 3)) & 0xFF,
            ((lut[values[14]] << 5) | (lut[values[15]])) & 0xFF,
        ]
    )
