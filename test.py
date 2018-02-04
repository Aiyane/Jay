#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from application import Jay, render_template

app = Jay()


@app.route('/')
def index():
    return 'Hello!'


@app.route('/students/')
def student():
    people1 = {"name": "张三", "age": "18", "major": "计算机"}
    people2 = {"name": "李四", "age": "19", "major": "金融"}
    people3 = {"name": "王五", "age": "20", "major": "法律"}

    many_people = [
        people1,
        people2,
        people3
    ]
    return render_template("model.html", many_people=many_people)


@app.route('/hello')
def hello():
    return 'Hello, world!'


@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s" % name


if __name__ == "__main__":
    app.run()
