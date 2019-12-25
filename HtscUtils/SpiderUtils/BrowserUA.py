# -*- coding: utf-8 -*-
# 浏览器UA生成模块

from fake_useragent import UserAgent

"""
使用说明：
此模块为浏览器ua获取模块，供爬虫开发设置请求头中的User-Agent字段
属性： user_agent --> 随机获取一个浏览器ua，类型为字符串
    ie，chrome，firefox属性分别返回对应浏览器内核随机版本的User-Agent
"""


class BrowserUA(object):
    def __init__(self):
        self.ua = UserAgent()

    @property
    def user_agent(self):
        return self.ua.random

    @property
    def ie(self):
        return self.ua.ie

    @property
    def chrome(self):
        return self.ua.chrome

    @property
    def firefox(self):
        return self.ua.firefox


if __name__ == '__main__':
    b = BrowserUA()
    print(b.user_agent)
