import json

from .constants import HttpStatus


class RequestHandler:
    def __init__(self, routes):
        self.routes = routes

    def process_request(self, request, path, method, headers, body):
        route = (path, method)
        if route in self.routes:
            handler = self.routes[route]
            try:
                content_length = int(headers.get("Content-Length", 0))
                if hasattr(body, "read"):
                    body_raw = body.read(content_length)
                    body_data = json.loads(body_raw.decode("utf-8"))
                else:
                    raise ValueError("Unsupported body format")
                return handler(request, body_data), HttpStatus.OK
            except json.JSONDecodeError:
                return "Invalid JSON", HttpStatus.BAD_REQUEST
            except Exception as e:
                return str(e), HttpStatus.INTERNAL_SERVER
        else:
            return "Not Found", HttpStatus.NOT_FOUND
