#!/usr/bin/env python3
# coding: utf-8
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class Jay(object):
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
        self.status = 0

    def app(self, environ, start_response):
        self.env = environ
        self.path = environ['PATH_INFO']

        return self._app(environ, start_response)

    def _app(self, environ, start_response):
        """实际的application, 将外部的函数装换成一个符合WSGI接口的application"""
        self.status = '200 OK'
        no_param_has_match = True  # 是否匹配到无参数的

        try:  # 无参数的
            url = tranfer_out_url(environ['PATH_INFO'])
            applications = self.path_info[url]
        except KeyError:
            try:
                url = tranfer_out_url(environ['PATH_INFO'] + '/')
                applications = self.path_info[url]
            except KeyError:
                no_param_has_match = False
                self.has_param_url(environ)

        if no_param_has_match:  # 匹配到无参数的
            if isinstance(applications[1], tuple):
                self.status = '404 no found'
                self.content = self.NotFindPage.encode("utf8")
            else:
                application = applications[0]
                self.content = application().encode("utf8")

        response_headers = [('Content-type', 'text/html;charset=utf8'),
                            ('Content-Length', str(len(self.content)))]
        start_response(self.status, response_headers)
        return [self.content]

    def has_param_url(self, environ):
        try:  # 有'<param>'参数的
            urls = environ['PATH_INFO'].split("/")
            param = urls[-1]
            url = tranfer_out_url('/'.join(urls[:-1]))
            applications = self.path_info[url]
            n = applications[1][0]

            if n == 0:
                raise KeyError

            if n == 2:
                param = int(param)
            elif n == 3:
                param = float(param)
            else:
                param = tranfer_str(param)

            application = applications[0]
            self.content = application(param).encode("utf8")

        except KeyError:  # 最后也没有返回404
            self.status = '404 no found'
            self.content = self.NotFindPage.encode("utf8")

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

        print("A server is running", self.remote_addr[:-1] + ":" + str(self.server_port) + "/ ...")
        server.serve_forever()

    def route(self, path):
        """路由装饰器, 保存外部application与path关系"""

        def wrapper(application):
            n = 0
            need_path = path

            if "<" in path:  # 如果在url中有参数
                need_path, keys = path.split("/<", 1)

                if ":" in keys:
                    cls, _param = keys.split(":")
                    cls = cls.strip()
                    if cls == "int":
                        n = (2, _param[:-1])
                    elif cls == "float":
                        n = (3, _param[:-1])
                else:
                    n = (1, keys[:-1])

            need_path = tranfer_url(need_path)
            self.path_info[need_path] = application, n

        return wrapper

    def test_request_context(self):
        return RequestContext(self.path_info)


class RequestContext(object):

    def __init__(self, path_info):
        self.path_info = path_info

    def __enter__(self):
        global mapping
        _path_info_ = dict((v, k) for k, v in self.path_info.items())
        mapping = dict(
            (k[0].__name__, (path, k[1]))
            for k, path in _path_info_.items()
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        mapping.clear()


def url_for(func_name, **keywords):
    string = ''
    tail = ''
    for k, v in keywords.items():
        try:
            if mapping[func_name][1][1] == k:
                tail += "/" + str(v)
                continue
        except TypeError:
            pass
        string += k + "=" + str(v) + "&"

    if string:
        return mapping[func_name][0] + tail + "?" + tranfer_url(string[:-1])
    return mapping[func_name][0] + tail


class ServerException(Exception):
    pass


class PortException(ServerException):
    pass


def tranfer_url(url):
    from urllib.parse import quote  # 转码url
    return quote(url, safe='/:?=')


def tranfer_str(url):
    # 解码url, 默认url会被转换成ascii, 显示时会解码成iso-8859-1格式
    # 这里要把它再解码转码成utf-8
    # 为啥WSGIRequestHandler的作者要转成iso-8859-1 ??? 标准库也这么坑人...
    return url.encode("iso-8859-1").decode('utf8')


def tranfer_out_url(url):
    from urllib.parse import quote  # 转码url
    # 转码url, 默认url会被转换成ascii, 显示时会解码成iso-8859-1格式
    # 这里要把它再解码转码成url
    # 为啥WSGIRequestHandler的作者要转成iso-8859-1 ??? 标准库也这么坑人...
    return quote(url.encode("iso-8859-1"), safe='/:?=')
