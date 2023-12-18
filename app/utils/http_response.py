from flask import jsonify


class HttpResponse:

    __slots__ = ("key", "value", "status",)

    def __init__(self, key=None, value=None, status=None) -> None:
        self.key = key
        self.value = value
        self.status = status

    def __create_http_response(self):
        return {self.key: self.value, "status": self.status}

    def http_response(self):
        return jsonify(self.__create_http_response()), self.status