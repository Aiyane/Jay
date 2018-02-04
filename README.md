## Jay

准备写一个类似于flask的web框架

### 测试

目前已写出一个小玩具, 在根目录下linux运行 `python3 test.py`或者windows安装了python3的运行 `python test.py` 打开浏览器输入 `http://localhost:8080/` 或者 `http://localhost:8080/hello` 即可.

### 目前用法

```py

from application import Jay, request

app = Jay()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/hello', methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return 'Hello, world!'

@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s!" % name

@app.route('/my/<int:n>')
def my(n):
    num = n/100
    return "your level is " + str(num)

if __name__ == "__main__":
    app.run()
```

`<cls:param>`这种写法现在支持int, float, 默认为str, 并不区分斜线, 支持对访问的方法判断

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

函数url_for可以获取application对应的url, 具体用法如下

```py
from application import Jay, url_for

app = Jay()


@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s" % name


@app.route('/')
def index():
    return "Hello, world!"


@app.route('/my 唉/<int:n>')
def my(n):
    num = n / 100
    return "比率为 " + str(num)


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for("index", name="Aiyane"))
        print(url_for("my", n=5))
        print(url_for("hello_world", name="aiyane", age=16))
```

会将参数当作url的参数结合进去, 而在application中定义的变量则会以'/'的形式接在url之后, 以上结果为

```
/?name=Aiyane
/my%20%E5%94%89/5
/hello/aiyane?age=16
```

