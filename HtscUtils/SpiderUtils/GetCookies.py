# -*- coding: utf-8 -*-
# 自定义request对象

from scrapy.http.cookies import CookieJar
from scrapy.http.request import Request

"""
从响应中获取cookies，适用于scrapy框架
在spider.py中调用，调用示例：
from HtscUtils.SpiderUtils.GetCookies import get_cookies

def parse(self, response):
        cookies_ = get_cookies(response)
        yield Request(
            url='https://...',
            method='GET',
            cookies=cookies_,
            callback=self.item_parse
        )

"""


def get_cookies(response):
    cookie_obj = CookieJar()
    cookie_obj.extract_cookies(response=response, request=response.request)
    return cookie_obj.extract_cookies
