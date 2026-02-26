from enum import IntEnum, auto

SERVER_URL = "https://messenger-s0tl.onrender.com/"
TIMEOUT = 5
MAX_PAYLOAD_LENGTH = 254

class Status(IntEnum):
    ASSOCIATE_SUCCESS = auto()
    ASSOCIATE_FAIL = auto()

    GOT_RESPONSE = auto()
    EMPTY_BUFFER = auto()

    PUSH_SUCCESS = auto()
    BUFFER_FULL = auto()
    INVALID_LENGTH = auto()