## Jay

准备写一个类似于flask的web框架

### 测试

目前已写出一个小玩具, 在根目录下linux运行 `python3 test.py`或者windows安装了python3的运行 `python test.py` 打开浏览器输入 `http://localhost:8080/` 或者 `http://localhost:8080/hello` 即可.

```py

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
    return "Hello %s!" % name


if __name__ == "__main__":
    app.run()
```

### 说明

```py
@app.route('/index')
def index():
    return 'Index Page'

@app.route('/hello/')
def index():
    return 'Hello!'
```
上述两种url风格, 区别是末尾是否有'/', 本框架的设计与主流框架保持一致, 在第一种写法中, 在客户端url末尾不加'/'可以正常访问, 在客户端url末尾加上'/'会报404错误. 在第二种写法中, 在客户端输入url时末尾加不加'/'都可以访问.

### 目前用法
