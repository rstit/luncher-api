from flask import request
from flask.views import MethodView


class Request:
    def __getattr__(self, item):
        return getattr(request, item)


class APIView(MethodView):
    def __init__(self, request) -> None:
        self.request = request or Request()
