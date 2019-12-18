# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
import json
from copy import deepcopy
import requests
from requests.adapters import HTTPAdapter
from .s3_upload import UploatS3
import re
from lxml import etree

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))


class NhsaSpider(scrapy.Spider):
    name = 'nhsa'
    allowed_domains = ['nhsa.gov.cn']
    start_urls = ['http://www.nhsa.gov.cn/col/col37/index.html', 'http://www.nhsa.gov.cn/col/col38/index.html']
    base_url = 'http://www.nhsa.gov.cn'

    def parse(self, response):
        # print(response)
        ajax_url = 'http://www.nhsa.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=1000&perpage=1000'
        form_li = [
            {
                'col': '1',
                'appid': '1',
                'webid': '1',
                'path': '/',
                'columnid': '37',
                'sourceContentType': '1',
                'unitid': '753',
                'webname': '国家医疗保障局',
                'permissiontype': '0'
            },
            {
                'col': '1',
                'appid': '1',
                'webid': '1',
                'path': '/',
                'columnid': '38',
                'sourceContentType': '1',
                'unitid': '753',
                'webname': '国家医疗保障局',
                'permissiontype': '0'
            }
        ]
        for form_data in form_li:
            yield FormRequest(url=ajax_url, formdata=form_data, callback=self.parse_list)

    def parse_list(self, response):
        # print(response.text)
        tree = etree.HTML(response.text)
        href_li = tree.xpath('//recordset/record//a/@href')
        # print(href_li)
        for href in href_li:
            if href.startswith("http"):
                url = href
            else:
                url = self.base_url + href
                # print(url)
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = {'main': {}, 'ass': []}
        item_main = {}
        indexid = response.request.url.split('/')[-1]
        text_link = ''
        if '<title>' not in response.text:
            resp = requests.get(response.request.url).content.decode('utf-8')
            response = etree.HTML(resp)
            title_ = response.xpath('//title/text()')
            if title_:
                title = title_[0].strip()
            else:
                title_li = response.xpath('//div[@class="atricle-title"]/text()')
                title = ''.join(title_li).strip()
            # pub_date = response.xpath('//div[@class="sub"]/span[1]/text()').extract_first()
            try:
                pub_date = re.findall(r'日期：\d{4}-\d{1,2}-\d{1,2}', resp)[0].split('：')[-1]
            except:
                pub_date = ''
                # print('出错!{}'.format(response.request.url))
                # print(response.text)
            text_div = response.xpath('//div[@id="zoom"]//text()')
            text_str = ' '.join(text_div).strip()
            if text_str:
                t = title + '.txt'
                s3u = UploatS3()
                text_link = s3u.uploat(text_str.encode('utf-8'), t, 'nhsa', pub_date.replace('-', '/'), indexid)
            annex_name = response.xpath('//div[@id="zoom"]//a/text()')
            annex_url = [self.base_url + i for i in response.xpath('//div[@id="zoom"]//a/@href')]
        else:
            title_ = response.xpath('//title/text()').extract_first()
            if title_:
                title = title_.strip()
            else:
                title_li = response.xpath('//div[@class="atricle-title"]/text()').extract()
                title = ''.join(title_li).strip()
            # pub_date = response.xpath('//div[@class="sub"]/span[1]/text()').extract_first()
            try:
                pub_date = re.findall(r'日期：\d{4}-\d{1,2}-\d{1,2}', response.text)[0].split('：')[-1]
            except:
                pub_date = ''
                # print('出错！{}'.format(response.request.url))
                # print(response.text)
            text_div = response.xpath('//div[@id="zoom"]')
            text_str = ' '.join(text_div.xpath('.//text()').extract()).strip()
            if text_str:
                t = title + '.txt'
                s3u = UploatS3()
                text_link = s3u.uploat(text_str.encode('utf-8'), t, 'nhsa', pub_date.replace('-', '/'), indexid)
            annex_name = text_div.xpath('.//a/text()').extract()
            annex_url = [self.base_url + i for i in text_div.xpath('.//a/@href').extract()]
        if annex_name and annex_url:
            annex_dict = dict(zip(annex_name, annex_url))
            # print('附件对应关系：{}'.format(annex_dict))
            for name, f_url in annex_dict.items():
                item_ass = {}
                if not re.findall(r'.*\..*', name):
                    name = name + '.html'
                    item_ass['linktype'] = 0
                else:
                    item_ass['linktype'] = 1

                content = s.get(f_url).content
                s3u = UploatS3()
                s3_url = s3u.uploat(content, name, 'nhsa', pub_date.replace('-', '/'), indexid)
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
        item_main['recordid'] = '国家医疗保障局'
        item['main'] = item_main
        # print(item)
        yield item
