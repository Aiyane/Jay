#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPResquestHandler
import socket


class WSGIResquestHandler(BaseHTTPResquestHandler):
    pass


def select_ip_version(host, port):
    if ':' in host and hasattr(socket, 'AF_INET6'):
        return socket.AF_INET6
    return socket.AF_INET


class BaseWSGIserver(HTTPServer):
    """
    docstring for BaseWSGIserver
    """
    def __init__(self, host, port, app, handler=None):
        if handler is None:
            handler = WSGIResquestHandler

        self.address = select_ip_version(host, port)
