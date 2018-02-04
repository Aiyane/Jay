#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from application import Jay

app = Jay()


@app.route('/')
def index():
    return 'Hello!'


@app.route('/hello')
def hello():
    return 'Hello, world!'


@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s" % name


if __name__ == "__main__":
    app.run()
