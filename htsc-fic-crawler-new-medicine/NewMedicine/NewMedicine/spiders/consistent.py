# -*- coding: utf-8 -*-
import scrapy
import re
import json
import requests
import time
from selenium.webdriver import Chrome, ChromeOptions
from .s3_upload import UploatS3


def consistent_cookie():
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)
    driver.get('http://www.cde.org.cn/news.do?method=news_index_yzxpj')
    time.sleep(2)
    driver.maximize_window()
    time.sleep(2)
    cookie = driver.get_cookies()
    driver.quit()
    cookies = ''
    for i in cookie:
        cookies += (i['name'] + '=' + i['value']) + '; '
    return cookies


def get_s3url(f_url, headers, name, medicine_name):
    resp = requests.get(f_url, headers=headers)
    if resp.status_code != 200:
        return False
    content = resp.content
    s3u = UploatS3()
    s3_url = s3u.uploat(content, name, 'consistent', medicine_name)
    return s3_url


class ConsistentSpider(scrapy.Spider):
    name = 'consistent'
    allowed_domains = ['cde.org.cn']
    start_urls = ['http://www.cde.org.cn/news.do?method=news_index_yzxpj']
    base_url = 'http://www.cde.org.cn/'
    headers = {
        'Host': 'www.cde.org.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': ''
    }
    data = {
        'acceptid': '',
        'currentPageNumber': '1',
        'pageMaxNumber': '',
        'totalPageCount': '',
        'pageroffset': '20',
        'pageMaxNum': '',
        'pagenum': '1'
    }

    def start_requests(self):
        self.headers['Cookie'] = consistent_cookie()
        s_url = 'http://www.cde.org.cn/yzxpjNotice.do?method=yzxpjNoticeList'
        # print(self.headers)
        yield scrapy.Request(url=s_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # print(response.request.headers)
        totalpage = response.xpath('//td[@id="pageNumber"]/font[2]/text()').extract()
        maxcount = re.findall(r'>(\d*)</font>条记录', response.text)[0]
        print(maxcount)
        self.data['pageMaxNumber'] = maxcount
        self.data['pageMaxNum'] = maxcount
        self.data['totalPageCount'] = totalpage
        yield scrapy.FormRequest(method='post', url='http://www.cde.org.cn/yzxpjNotice.do?method=yzxpjNoticeList',
                                 headers=self.headers, formdata=self.data, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.text)
        tr_li = response.xpath('//tr[@class="newsindex"]')
        for tr in tr_li:
            item = {}
            item['ordernumber'] = tr.xpath('./td[1]/text()').extract_first()
            item['acceptancenumber'] = tr.xpath('./td[2]/text()').extract_first().strip()
            item['medicinename'] = tr.xpath('./td[3]/text()').extract_first()
            info_url = self.base_url + tr.xpath('./td[4]/a/@href').extract_first()
            instruction_url = self.base_url + tr.xpath('./td[5]/a/@href').extract_first()
            while True:
                info = get_s3url(info_url, headers=self.headers, name=item['medicinename'] + '-信息公开.doc',
                                 medicine_name=item['medicinename'])
                instruction = get_s3url(instruction_url, headers=self.headers, name=item['medicinename'] + '-说明书.doc',
                                        medicine_name=item['medicinename'])
                if info and instruction:
                    break
                else:
                    self.headers['Cookie'] = consistent_cookie()
            item['info'] = info
            item['instruction'] = instruction
            item['remark'] = 0
            item['isvalid'] = 1
            item['resourceid'] = '爬虫'
            item['recordid'] = '一致性评价'
            print(item)
            yield item
