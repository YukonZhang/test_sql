# -*- coding: utf-8 -*-
import scrapy
import re
import json
from .s3_upload import UploatS3
import requests
from requests.adapters import HTTPAdapter
import js2py
from lxml import etree
import execjs
from MedicineSpider.proxies import ip_redis

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))


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


class NmpaSpider(scrapy.Spider):
    name = 'nmpa'
    allowed_domains = ['nmpa.gov.cn']
    start_urls = [
        'http://www.nmpa.gov.cn/WS04/CL2170/',
        'http://www.nmpa.gov.cn/WS04/CL2178/',
        'http://www.nmpa.gov.cn/WS04/CL2171/',
        'http://www.nmpa.gov.cn/WS04/CL2179/']
    base_url = 'http://www.nmpa.gov.cn/WS04'
    file_base = 'http://www.nmpa.gov.cn'

    # num = 0

    def parse(self, response):
        # if response.status != 200:
        #     cookies = get_cookie(response.request.url)
        #     yield scrapy.Request(url=response.request.url, callback=self.parse, cookies=cookies, dont_filter=True)
        # # print(t)
        # else:
        # yield scrapy.Request(url=response.request.url, callback=self.parse_page)
        t = response.text.encode('cp1252').decode('gbk')
        page = re.findall(r'共(\d*)页', t)[0]
        print(page)
        for i in range(int(page)):
            if i == 0:
                u = response.request.url + 'index.html'
            else:
                u = response.request.url + 'index_{}.html'.format(i)
            # print(u)
            yield scrapy.Request(url=u, callback=self.parse_page)

    def parse_page(self, response):
        if '<TITLE>' not in response.text:
            yield scrapy.Request(url=response.request.url, callback=self.parse_page, dont_filter=True)
        a_li = response.xpath('//table[3]/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr//a/@href').extract()
        for href in a_li:
            url = self.base_url + href.replace('..', '')
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item = {'main': {}, 'ass': []}
        item_main = {}
        if '<title>' not in response.text:
            yield scrapy.Request(url=response.request.url, callback=self.parse_item, dont_filter=True)
        else:
            indexid = response.request.url.split('/')[-1]
            title = response.xpath('//title/text()').extract_first()
            pub_date = re.findall(r'\d{4}年\d{1,2}月\d{1,2}', response.text)[0]
            pub_date = pub_date.replace('年', '-').replace('月', '-')
            # print(title + ' ' + pub_date)
            text_li = response.xpath('//td[@class="articlecontent3"]//text()').extract()
            text_str = ' '.join(text_li)
            text_link = ''
            if text_str:
                t = title + '.txt'
                s3u = UploatS3()
                text_link = s3u.uploat(text_str.encode('utf-8'), t, 'nmpa', pub_date.replace('-', '/'), indexid)
            annex_name = response.xpath('//td[@class="articlecontent3"]//a/text()').extract()
            annex_url = [self.file_base + i for i in
                         response.xpath('//td[@class="articlecontent3"]//a/@href').extract()]
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
                    proxies = {'http': ip_redis().random()}
                    content = s.get(f_url, proxies=proxies).content
                    s3u = UploatS3()
                    s3_url = s3u.uploat(content, name, 'nmpa', pub_date.replace('-', '/'), indexid)
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
            item_main['recordid'] = '国家药品监督管理局'
            item['main'] = item_main
            # print(item)
            print(title)
            yield item
