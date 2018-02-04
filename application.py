#!/usr/bin/env python3
# coding: utf-8
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class Application(object):
    def __init__(self):
        self.env = {}
        self.start = None
        self.content = ''
        self.server_class = WSGIServer
        self.handler_class = WSGIRequestHandler
        self.path_info = {}

    def app(self, environ, start_response):
        status = '200 OK'
        application = self.path_info[environ['PATH_INFO']]
        self.content = application().encode("utf8")
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(self.content)))]
        start_response(status, response_headers)
        return [self.content]

    def make_server(self, host='', port=8080, server_class=None, handler_class=None):
        if server_class is None:
            server_class = self.server_class
        if handler_class is None:
            handler_class = self.handler_class
        host = host
        if port < 1000 or port > 9999:
            raise PortException('The port is %r, isn\'t legal port' % port)
        port = port
        server = server_class((host, port), handler_class)
        server.set_app(self.app)
        return server

    def run(self, host='', port=8080, server_class=None, handler_class=None):
        server = self.make_server(host, port, server_class, handler_class)
        sa = server.socket.getsockname()
        print("A server is running", sa[0], "port:", sa[1], "...")
        server.serve_forever()

    def route(self, path):
        def wrapper(application):
            self.path_info[path] = application
        return wrapper


class ServerException(Exception):
    pass


class PortException(ServerException):
    pass


app = Application()


@app.route('/')
def hello_world():
    return "Hello, world!"


if __name__ == '__main__':
    app.run()
