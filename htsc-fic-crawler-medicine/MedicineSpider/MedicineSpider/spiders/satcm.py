# -*- coding: utf-8 -*-
import re

import scrapy


class SatcmSpider(scrapy.Spider):
    name = 'satcm'
    allowed_domains = ['satcm.gov.cn']
    start_urls = ['http://www.satcm.gov.cn/a/zcwj/', 'http://www.satcm.gov.cn/a/zcjd/']
    base_url = 'http://www.satcm.gov.cn'

    def parse(self, response):
        end_page = response.xpath('//a[contains(text(), "尾页")]/@href').extract_first()
        page = int(re.findall(r'_(\d*).html', end_page)[0])
        print(page)
        for i in range(1, page + 1):
            if i == 1:
                url = response.request.url + 'index.html'
            else:
                url = response.request.url + 'index_{}.html'.format(i)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        href_li = response.xpath('//table//li/a/@href').extract()
        for href in href_li:
            if href.startswith('http'):
                url = href
            else:
                url = self.base_url + href
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item = {'main': {}, 'ass': []}
        item_main = {}
        title = response.xpath('//title/text()').extract_first().strip()
        print(title)
        yield item
