from http.server import HTTPServer
from .constants import HttpMethod
from functools import partial

from .handler_request import CustomHandler


class Server:
    routes = {}

    def route(self, path: str, method: HttpMethod):
        """
        A decorator to register dynamic routes.

        Args:
        path (str): The URL path for the route.
        method (str): The HTTP method (e.g., 'GET', 'POST') for the route.

        Returns:
        function: The decorated function to be registered for the given route and method.
        """

        def decorator(func):
            self.routes[(path, method)] = func
            return func

        return decorator

    def start(self, host="localhost", port=8080):
        """
        Starts the HTTP server to listen for incoming requests.

        Args:
            host (str): The host address for the server. Default is "localhost".
            port (int): The port number for the server to listen on. Default is 8080.

        Prints:
            A message indicating the server is running with the host and port.

        Starts an infinite loop to handle requests via the custom HTTP server.
        """
        custom_handler = partial(CustomHandler, routes=self.routes)
        server = HTTPServer((host, port), custom_handler)
        print(f"🚀 Server running at http://{host}:{port}")
        server.serve_forever()
