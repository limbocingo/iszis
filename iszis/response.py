from http import HTTPStatus
from json import dumps


class Response:
    """
    Takes you'r `JSON` and trasform it to an 
    HTTP readeable bytes object.

    Parameters of the class:
        - `json`: JSON value of the return.
        - `status`: The status that will be receveied. 
    """

    def __init__(self, json: list | dict, status: int = 200) -> None:
        """
        Transform you'r JSON to an HTTP
        readeble encoded text.
        """
        self.json = json
        self.status = status

    def response(self):
        """
        The encoded and formated HTTP text.
        """
        if not isinstance(self.json, dict) and not isinstance(self.json, dict):
            raise ValueError('Response JSON needs to by dictionary or array.')
        return f'HTTP/1.1 {self.status} {HTTPStatus(self.status).phrase}\r\nHTTP-Version: HTTP/1.1\r\nServer: Fassy rest-API\r\nAccept: application/json\r\nContent-Type: application/json\r\nContent-Lenght: {len(self.json) if self.json else 0}\r\n\r\n{dumps(self.json) if self.json else "null"}'.encode()