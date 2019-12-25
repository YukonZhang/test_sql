from flask import Flask
from .get_ip import Getter

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello'


# todo:获取随机可用代理
@app.route('/random')
def random():
    try:
        return Getter().random()
    except:
        return '暂无可用代理'

@app.route('/count')
def count():
    try:
        return '可用代理数量%s'%Getter().counts()
    except:
        return '暂无可用代理'



if __name__ == '__main__':
    app.run('127.0.0.1', '8000')
