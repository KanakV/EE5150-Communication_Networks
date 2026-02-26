from config import SERVER_URL, TIMEOUT
import requests
from protocol.frame import Frame

# Handle:
#   INVALID_LENGTH
#   MALFORMED_FRAME


class HTTPClient():
    def __init__(self):
        pass

    def get_response(self, frame: Frame):
        try:
            response = requests.post(
                    SERVER_URL,
                    json=frame.to_json(),
                    timeout=TIMEOUT
                )
            return Frame(**response.json())
        except (TimeoutError, ConnectionError):
            return Frame(type=0, message="ASSOCIATE_FAIL", id=frame.id)

