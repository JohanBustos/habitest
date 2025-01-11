from http.server import BaseHTTPRequestHandler
from .constants import HttpMethod
from .request_handler import RequestHandler
import json


class CustomHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, routes=None, **kwargs):
        self.handler = RequestHandler(routes or {})
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.handle_request(HttpMethod.GET)

    def do_POST(self):
        self.handle_request(HttpMethod.POST)

    def handle_request(self, method):
        response, status = self.handler.process_request(
            self, self.path, method, self.headers, self.rfile
        )
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))
