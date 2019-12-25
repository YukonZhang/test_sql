# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from HtscUtils.SpiderUtils.GetCookies import get_cookies

"""
以下为get_cookies在scrapy项目中的调用示例
"""


class LithPriceSpider(scrapy.Spider):
    name = 'spidername'
    allowed_domains = ['']
    start_urls = ['']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    def parse(self, response):
        cookies_ = get_cookies(response)
        yield Request(
            url='https://...',
            method='GET',
            cookies=cookies_,
            callback=self.item_parse
        )

    def item_parse(self):
        pass
