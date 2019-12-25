# -*- coding: utf-8 -*-
# 执行js代码模块

import js2py
import execjs
import os

"""
使用说明：
此模块为使用python执行js代码的模块。用于解决部分网站数据由js代码动态生成的问题
1. DealJS类接收两个参数。js_str为字符串形式的js代码，不传则默认为空字符串；
path为js文件路径（推荐使用绝对路径），此处js文件应是经过分析处理过的文件，
标准为：可单独执行，不应包含window和其他文件中对象（或变量）的引入，否则执行会报错。
        js文件中各函数参数应依据开发需求事先进行替换，或放入字符串以exec_func方法传参执行
2. 三种js执行方法。
   a. 执行js字符串（无需传参），  exec_str()
   b. 执行js函数（依照函数所需参数依次传参），  exec_func()
   c. 执行js文件，  exec_file()
"""


class DealJS(object):
    def __init__(self, js_str="", path=None):
        self.js_str = js_str
        self.path = path

    def exec_str(self):
        """
        执行js字符串
        :return:
        """
        ret = js2py.eval_js(self.js_str)
        return ret

    def exec_func(self, *args):
        """
        执行js函数， args用于函数传参
        :param args:
        :return:
        """
        func = js2py.eval_js(self.js_str)
        return func(*args)

    def exec_file(self):
        """
        执行js文件
        :return: 返回执行结果 context
        """
        with open(self.path)as f:
            js = f.read()
            context = js2py.EvalJs()
            context.execute(js)
            return context


# if __name__ == '__main__':
#     dj = DealJS('var a="hello"')
#     r = dj.exec_str()
#     print(r)
#
#     # dj = DealJS(js_str='function add(a,b) {return a+b}')
#     # ret = dj.exec_func(3, 5)
#     # print(ret)
#
#     # dj = DealJS(path='./test.js')
#     # c = dj.exec_file()
#     # print(c.guid1)
