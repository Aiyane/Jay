## Jay

准备写一个类似于flask的web框架

### 测试

目前已写出一个小玩具, 在根目录下linux运行 `python3 test.py`或者windows安装了python3的运行 `python test.py` 打开浏览器输入 `http://localhost:8080/` 或者 `http://localhost:8080/hello` 即可.

### 目前用法

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

