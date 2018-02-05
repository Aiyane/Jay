#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from application import Jay, url_for, request, render_template

app = Jay()


@app.route('/hello/<name>', methods=["GET", "POST"])
def hello_world(name):
    if request.method == "GET":
        return "Hello %s" % name


@app.route('/')
def index():
    return "Hello, world!"


@app.route('/my 唉/<int:n>')
def my(n):
    num = n / 100
    return "比率为 " + str(num)


@app.route('/students/')
def student():
    people1 = {"name": "张三", "age": "18", "major": "计算机"}
    people2 = {"name": "lisi", "age": "19", "major": "金融"}
    people3 = {"name": "王五", "age": "20", "major": "法律"}

    many_people = [
        people1,
        people2,
        people3
    ]
    return render_template("model.html", many_people=many_people, upper=my_upper)


@app.route('/base/')
def base():
    return render_template("kid.html")


def my_upper(name):
    return name.upper()


if __name__ == '__main__':
    app.run()
    # with app.test_request_context():
    #     print(url_for("index", name="Aiyane"))
    #     print(url_for("my", n=5))
    #     print(url_for("hello_world", name="aiyane", age=16))
