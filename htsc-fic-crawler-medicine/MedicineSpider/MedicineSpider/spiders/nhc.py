# -*- coding: utf-8 -*-
import time

import scrapy
from copy import deepcopy
import json
import re
import requests
from requests.adapters import HTTPAdapter
from .s3_upload import UploatS3
from urllib.parse import urlparse
from selenium.webdriver import Chrome

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))


class NhcSpider(scrapy.Spider):
    name = 'nhc'
    allowed_domains = ['nhc.gov.cn']
    start_urls = ['http://www.nhc.gov.cn/wjw/zcfg/list.shtml', 'http://www.nhc.gov.cn/wjw/zcjd/list.shtml']
    base_url = 'http://www.nhc.gov.cn'

    def parse(self, response):
        print(response.status)
        if response.status != 200:
            driver = Chrome()
            driver.get(response.request.url)
            time.sleep(2)
            href_li = driver.find_elements_by_xpath('//div[@class="list"]//li/a')
            for i in href_li:
                href = self.base_url + i.get_attribute('href')
                # print(href)
                yield scrapy.Request(url=href, callback=self.parse_item)
            page = re.findall(r"'page_div',(\d*),", driver.page_source)[0]
            driver.quit()
            print(page)
            for p in range(2, int(page) + 1):
                url = response.request.url.replace('list', 'list_{}'.format(p))
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse_page)
        else:
            href_li = response.xpath('//div[@class="list"]//li/a/@href').extract()
            for i in href_li:
                href = self.base_url + i
                # print(href)
                yield scrapy.Request(url=href, callback=self.parse_item)
            page = re.findall(r"'page_div',(\d*),", response.text)[0]
            print(page)
            for p in range(2, int(page) + 1):
                url = response.request.url.replace('list', 'list_{}'.format(p))
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        if response.status != 200:
            yield scrapy.Request(url=response.request.url, callback=self.parse_page, dont_filter=True)
        else:
            href_li = response.xpath('//div[@class="list"]//li/a/@href').extract()
            for i in href_li:
                href = self.base_url + i
                # print(href)
                yield scrapy.Request(url=href, callback=self.parse_item)

    def parse_item(self, response):
        if response.status != 200 or '<title>' not in response.text:
            yield scrapy.Request(url=response.request.url, callback=self.parse_item, dont_filter=True)
        else:
            item = {'main': {}, 'ass': []}
            item_main = {}
            indexid = response.request.url.split('/')[-1]
            body = response.xpath('//div[@class="list"]//text()').extract()
            body_str = ''.join(body)
            pub_ = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', body_str)
            # if not pub_:
            #     pub_ = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', requests.get(response.request.url).text)
            pub_date = pub_[0]
            # try:
            title = response.xpath('//title/text()').extract_first().strip()
            # except Exception:
            #     title = ''
            # if not title:
            # print(response.text)
            # else:
            # title = title
            # text_li = response.xpath('//div[@id="xw_box"]//p/text()').extract()
            # if not text_li:
            #     text_li = response.xpath('//div[@id="xw_box"]//text()').extract()
            # text = ' '.join(text_li).strip()
            t = title + '.html'
            s3u = UploatS3()
            text_link = s3u.uploat(response.text.encode('utf-8'), t, 'nhc', pub_date.replace('-', '/'), indexid)
            annex_name = response.xpath('//div[@id="xw_box"]//p/a/text()').extract()
            an_url = response.xpath('//div[@id="xw_box"]//p/a/@href').extract()
            annex_url = []
            for a_url in an_url:
                if a_url.startswith('http'):
                    url = a_url
                else:
                    r_url = response.request.url
                    url = '/'.join(r_url.split('/')[:-1]) + '/' + a_url
                annex_url.append(url)
            print(response.request.url)
            print(annex_url)
            if annex_name and annex_url:
                annex_dict = dict(zip(annex_name, annex_url))
                # print('附件对应关系：{}'.format(annex_dict))
                for name, f_url in annex_dict.items():
                    item_ass = {}
                    if re.findall(r'.*html', f_url):
                        name = name + '.html'
                        item_ass['linktype'] = 0
                    else:
                        item_ass['linktype'] = 1
                        name = name + '.' + f_url.split('.')[-1]
                    name = name.replace('/', '')
                    content = s.get(f_url).content
                    s3u = UploatS3()
                    s3_url = s3u.uploat(content, name, 'nhc', pub_date.replace('-', '/'), indexid)
                    item_ass['annexname'] = name
                    item_ass['policyid'] = indexid
                    item_ass['annexurl'] = s3_url
                    item['ass'].append(item_ass)
            item_main['policyid'] = indexid
            item_main['pubtime'] = pub_date
            item_main['title'] = title
            item_main['policybodyurl'] = text_link
            item_main['isvalid'] = 1
            item_main['resourceid'] = '爬虫'
            item_main['recordid'] = '卫生健康委员会'
            item['main'] = item_main
            # print(item['main']['title'] + '  {}'.format(item['main']['pubtime']))
            # print(item)
            # print(item['ass'])
            yield item
