# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
from scrapy.http import Response
import execjs
from lxml import etree
from .proxies import ip_redis


def get_cookie(url):
    cookies = {
        'FSSBBIl1UgzbN7N80S': '',
        'FSSBBIl1UgzbN7N80T': ''
    }
    with open('./MedicineSpider/js/getcookie.js', 'r', encoding='utf-8') as f:
        js1 = f.read()
        ecjs = execjs.compile(js1)
    rsq = requests.get(url)
    rsq.close()
    # print(rsq.cookies)
    # 第一次请求得到假的f80s,f80t,和metacontent
    F80S = rsq.cookies['FSSBBIl1UgzbN7N80S']
    F80T = rsq.cookies['FSSBBIl1UgzbN7N80T']
    rsqHtml = etree.HTML(rsq.text)
    meta = rsqHtml.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
    F80T_true = ecjs.call("getcookie", meta, F80T)
    cookies['FSSBBIl1UgzbN7N80S'] = F80S
    cookies['FSSBBIl1UgzbN7N80T'] = F80T_true
    return cookies


class MedicinespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MedicinespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if spider.name == 'nmpa':
            cookies = get_cookie(request.url)
            # request.headers['Connection'] = 'close'
            request.cookies = cookies
        if spider.name == 'satcm':
            proxies = ip_redis().random()
            request.meta['proxy'] = proxies
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # if spider.name == 'nmpa':
        #     response.text = response.text.encode('utf-8').decode('gbk')
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)