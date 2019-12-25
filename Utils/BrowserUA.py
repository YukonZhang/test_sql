# -*- coding: utf-8 -*-
# 浏览器UA生成模块

from fake_useragent import UserAgent


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
