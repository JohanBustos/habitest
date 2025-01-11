from unittest import mock
from server import Server, HttpMethod
from server.handler_request import CustomHandler
from http.server import BaseHTTPRequestHandler


def test_server_start_without_routes():
    app = Server()
    assert app.routes == {}


def test_server_route_decorator():
    app = Server()

    @app.route("/ping", HttpMethod.GET)
    def hello(request, body):
        return {"message": "pong"}

    assert app.routes == {("/ping", HttpMethod.GET): hello}
