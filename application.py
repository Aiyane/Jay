#!/usr/bin/env python3
# coding: utf-8
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class Application(object):

    NotFindPage = """\
    <html>
    <head>
        <meta charset="UTF-8">
        <title>404错误</title>
    </head>
    <body>
        <h1>404错误</h1>
        <p>没有此页面</p>
    </body>
    </html>
    """

    def __init__(self):
        self.remote_addr = ''
        self.server_port = 0
        self.env = {}
        self.start = None
        self.content = ''
        self.server_class = None
        self.handler_class = None
        self.path = ''
        self.path_info = {}

    def app(self, environ, start_response):
        self.env = environ
        self.path = environ['PATH_INFO']

        return self._app(environ, start_response)

    def _app(self, environ, start_response):
        """实际的application, 将外部的函数装换成一个符合WSGI接口的application"""
        status = '200 OK'

        try:  # 无参数的
            applications = self.path_info[environ['PATH_INFO']]

            if applications[1] != 0:
                raise KeyError

            application = applications[0]
            self.content = application().encode("utf8")

        except KeyError:
            try:  # 有'<param>'参数的
                urls = environ['PATH_INFO'].split("/")
                param = urls[-1]
                applications = self.path_info['/'.join(urls[:-1])]

                if applications[1] != 1:
                    raise KeyError

                application = applications[0]
                self.content = application(param).encode("utf8")

            except KeyError:  # 最后也没有返回404
                status = '404 '
                self.content = self.NotFindPage.encode("utf8")

        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(self.content)))]
        start_response(status, response_headers)
        return [self.content]

    def make_server(self, host, port, server_class, handler_class):
        """初始化服务器"""
        self.server_class = server_class
        self.handler_class = handler_class

        if host == '':
            self.remote_addr = 'http://127.0.0.1/'
        else:
            self.remote_addr = host

        if port < 1000 or port > 9999:
            raise PortException('The port is %r, isn\'t legal port' % port)
        self.server_port = port

        server = server_class((host, port), handler_class)

        server.set_app(self.app)  # 绑定application

        return server

    def run(self, host='', port=8080, server_class=WSGIServer, handler_class=WSGIRequestHandler):

        server = self.make_server(host, port, server_class, handler_class)  # 调用make_server

        print("A server is running", self.remote_addr, "port:", self.server_port, "...")
        server.serve_forever()

    def route(self, path):
        """路由装饰器, 保存外部application与path关系"""
        def wrapper(application):

            if "<" in path:  # 如果在url中有参数
                paths = path.split("/<", 1)
                self.path_info[paths[0]] = application, 1

            else:
                self.path_info[path] = application, 0
        return wrapper


class ServerException(Exception):
    pass


class PortException(ServerException):
    pass


app = Application()


@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s" % name


@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    app.run()
