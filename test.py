#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from application import Jay

app = Jay()


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/hello')
def hello():
    return 'Hello, world!'


if __name__ == "__main__":
    app.run()
