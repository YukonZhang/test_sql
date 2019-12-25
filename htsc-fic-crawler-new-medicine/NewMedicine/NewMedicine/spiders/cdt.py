# -*- coding: utf-8 -*-
import scrapy
import re
import json


class CdtSpider(scrapy.Spider):
    name = 'cdt'
    allowed_domains = ['chinadrugtrials.org.cn']
    start_urls = ['http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist']

    def parse(self, response):
        total = response.xpath('//div[@class="page_left"]/a[1]/text()').extract_first().strip()
        data = {
            'sort': 'desc',
            'sort2': 'desc',
            'rule': 'CTR',
            'currentpage': '1',
            'pagesize': '',
            'keywords': '',
            'reg_no': 'CTR'
        }
        data['pagesize'] = str(total)
        yield scrapy.FormRequest(method='post', url=response.request.url, formdata=data, callback=self.parse_item)

    def parse_item(self, response):
        tr_li = response.xpath('//tr[@style=" color:#535353"]')
        for tr in tr_li:
            item = {}
            item['registnumber'] = tr.xpath('./td[2]/a/text()').extract_first().strip()
            item['teststatus'] = tr.xpath('./td[3]/a/text()').extract_first().strip()
            item['medicinename'] = tr.xpath('./td[4]/a/text()').extract_first().strip()
            item['indication'] = tr.xpath('./td[5]/a/text()').extract_first().strip()
            item['testproblem'] = tr.xpath('./td[6]/a/text()').extract_first().strip()
            item['isvalid'] = 1
            item['resourceid'] = '爬虫'
            item['recordid'] = '临床试验最新记录'
            yield item
