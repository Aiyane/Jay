#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import sys


class WSGIResquestHandler(BaseHTTPRequestHandler):
    def make_environ(self):
        def shutdown_server():
            self.server.shutdown_signal = True

        url_scheme = 'http'

        environ = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.input': self.rfile,
            'wsgi.errors': sys.stderr,
            'wsgi.run_once': False,
            'werkzeug.server.shutdown': shutdown_server,
            'SERVER_SOFTWARE': self.server_version,
            'REQUEST_METHOD': self.command,
            'SCRIPT_NAME': '',
            'REMOTE_ADDR': self.address_string(),
            'SERVER_NAME': self.server.server_address[0],
            'SERVER_PORT': str(self.server.server_address[1]),
            'SERVER_PROTOCOL': self.request_version
        }
        for key, value in self.headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = 'HTTP_' + key
            environ[key] = value

        if environ.get('HTTP_TRANSFER_ENCODING',
                       '').strip().lower() == 'chunked':
            environ['wsgi.input_terminsteed'] = True

        return environ

    def handle(self):
        """Handles a request ignoring dropped connections."""
        rv = None
        try:
            rv = BaseHTTPRequestHandler.handle(self)
        except (socket.error, socket.timeout) as e:
            self.connection_dropped(e)
        except Exception:
            if self.server.ssl_context is None:
                raise
        if self.server.shutdown_signal:
            self.initiate_shutdown()
        return rv


def select_ip_version(host, port):
    if ':' in host and hasattr(socket, 'AF_INET6'):
        return socket.AF_INET6
    return socket.AF_INET


def get_sockaddr(host, port, family):
    try:
        res = socket.getaddrinfo(host, port, family, socket.SOCK_STREAM,
                                 socket.SOL_TCP)
    except socket.gaierror:
        return host, port
    return res[0][4]


class BaseWSGIServer(HTTPServer):
    """
    docstring for BaseWSGIserver
    """

    def __init__(self, host, port, app, handler=None):
        if handler is None:
            handler = WSGIResquestHandler

        self.address_family = select_ip_version(host, port)

        # 初始化
        HTTPServer.__init__(self,
                            get_sockaddr(host, int(port), self.address_family),
                            handler)

        self.app = app
        self.host = host
        self.port = self.socket.getsockname()[1]

    def serve_forever(self):
        try:
            HTTPServer.serve_forever(self)
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()

    def get_request(self):
        con, info = self.socket.accept()
        return con, info


def make_server(host=None, port=None, app=None, request_handler=None):
    return BaseWSGIServer(host, port, app, request_handler)


def _log(type, message, *args, **kwargs):
    global _logger
    if _logger is None:
        import logging
        _logger = logging.getLogger('Jay')
        if not logging.root.handlers and _logger.level == logging.NOTSET:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)


def run_simple(hostname, port, application, request_handler):
    if not isinstance(port, int):
        raise TypeError('por must be an integer')

    def inner():
        srv = make_server(hostname, port, application, request_handler)
        srv.serve_forever()

    def log_startup(sock):
        # 打印信息
        display_hostname = hostname not in ('',
                                            '*') and hostname or 'localhost'
        if ':' in display_hostname:
            display_hostname = '[%s]' % display_hostname
        quit_msg = '(Press CTRL+C to quit)'
        port = sock.getsockname()[1]
        _log('info', ' * Running on %s://%s:%d/ %s', 'http', display_hostname,
             port, quit_msg)

    inner()
