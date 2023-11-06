import inspect

from parse import parse
from webob import Request, Response


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):
        assert path not in self.routes, "Such route already exists."

        def wrapper(handler):
            self.routes[path] = handler

        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not Found.'

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is None:
            self.default_response(response)

        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)
            if not handler:
                raise AttributeError("Method not allowed", request.method)

        handler(request, response, **kwargs)

        return response