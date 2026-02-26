#

# This is what the user interacts with
# Performs the following high level tasks:
#   Create connection to server (calls an object that maintains the connection)
#   Sends messages (only inputs destination id & message)
#   Gets messages from server (sends to API)
# Also maintains the http link

from client.httpClient import HTTPClient
from protocol.frame import Frame
from config import Status

class User():
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.http = HTTPClient()
        self.associated = False
        # print(f"User {self.user_id} created successfully")
    
    def associate(self):
        # Returns the JSON/Frame response form server
        associateResponse = self.http.get_response(
            Frame(
                type=0,
                message="ASSOCIATE",
                id=self.user_id
            )
        )
        
        if associateResponse.message == "ASSOCIATE_SUCCESS":
            self.associated = True
            # print(f"User {self.user_id} associated succesfully")
            return Status.ASSOCIATE_SUCCESS
        
        return Status.ASSOCIATE_FAIL
            
    def get(self) -> str | None:
        getResponse = self.http.get_response(
            Frame(
                type=1,
                message="GET",
                id=self.user_id
            )
        )

        status = getResponse.message
        if status == "GET_RESPONSE":
            # IF VALID RESPONSE, SEND PAYLOAD AND SENDER ID
            return Status.GOT_RESPONSE, getResponse.payload, getResponse.id2
        elif status == "BUFFER_EMPTY":
            return Status.EMPTY_BUFFER, None, None
        elif status == "ASSOCIATE_FAIL":
            self.associated = False
            return Status.ASSOCIATE_FAIL, None, None
        
    def send(self, reciepient_id: int, message: str):
        if self.associated:
            sendResponse = self.http.get_response(
                Frame(
                    type=2,
                    message="PUSH",
                    id=self.user_id,
                    id2=reciepient_id,
                    payload=message
                )
            )

            status = sendResponse.message
            status = "ASSOCIATE_FAIL"
            if status == "PUSH_SUCCESS":
                return Status.PUSH_SUCCESS
            elif status == "BUFFER_FULL":
                return Status.BUFFER_FULL
            elif status == "INVALID_LENGTH":
                return Status.INVALID_LENGTH
            elif status == "ASSOCIATE_FAIL":
                self.associated = False
                return Status.ASSOCIATE_FAIL