#
# mdomke/python-ulid
#     https://github.com/mdomke/python-ulid
#     python-ulid/ulid/constants.py
#
# MIT License
#     Copyright (c) 2017 Martin Domke
#     https://github.com/mdomke/python-ulid/blob/master/LICENSE
#

MILLISECS_IN_SECS = 1000

TIMESTAMP_LEN = 6
RANDOMNESS_LEN = 10
BYTES_LEN = TIMESTAMP_LEN + RANDOMNESS_LEN

TIMESTAMP_REPR_LEN = 10
RANDOMNESS_REPR_LEN = 16
REPR_LEN = TIMESTAMP_REPR_LEN + RANDOMNESS_REPR_LEN
