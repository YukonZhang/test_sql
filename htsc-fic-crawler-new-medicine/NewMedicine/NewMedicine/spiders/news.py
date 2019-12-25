# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome, ChromeOptions
import time
import re


def new_cookie():
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)
    driver.get('http://www.cde.org.cn/news.do?method=changePage&pageName=service&frameStr=3')
    time.sleep(2)
    driver.maximize_window()
    time.sleep(2)
    cookie = driver.get_cookies()
    driver.quit()
    cookies = ''
    for i in cookie:
        cookies += (i['name'] + '=' + i['value']) + '; '
    return cookies


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['cde.org.cn']
    start_urls = ['http://www.cde.org.cn/news.do?method=changePage&pageName=service&frameStr=3']
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
        'checktype': '1',
        'pagetotal': '',
        'statenow': '0',
        'year': '全部',
        'currentPageNumber': '1',
        'pageMaxNumber': '',
        'totalPageCount': '',
        'pageroffset': '',
        'pageMaxNum': '',
        'pagenum': '1'
    }

    def start_requests(self):
        self.headers['Cookie'] = new_cookie()
        s_url = 'http://www.cde.org.cn/transparent.do?method=list'
        yield scrapy.FormRequest(url=s_url, callback=self.parse, headers=self.headers, formdata=self.data)

    def parse(self, response):
        maxcount = re.findall(r'>(\d*)</font>条记录', response.text)[0]
        # print(maxcount)
        self.data['pageMaxNumber'] = maxcount
        self.data['pageMaxNum'] = maxcount
        self.data['pagetotal'] = maxcount
        yield scrapy.FormRequest(method='post', url='http://www.cde.org.cn/transparent.do?method=list',
                                 headers=self.headers, formdata=self.data, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.request.cookies)
        tr_li = response.xpath('//tr[@height="30"]')
        print(len(tr_li))
        for tr in tr_li:
            item = {}
            item['acceptancenumber'] = tr.xpath('./td[1]/text()').extract_first()
            item['medicinename'] = tr.xpath('./td[2]/text()').extract_first()
            item['medicinetype'] = tr.xpath('./td[3]/text()').extract_first()
            item['applytype'] = tr.xpath('./td[4]/text()').extract_first()
            item['registtype'] = tr.xpath('./td[5]/text()').extract_first()
            item['businessname'] = tr.xpath('./td[6]/text()').extract_first().strip()
            item['undertaketype'] = tr.xpath('./td[7]/text()').extract_first().strip()
            item['isvalid'] = 1
            item['resourceid'] = '爬虫'
            item['recordid'] = '新药申请数据'
            print(item)
            yield item


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)
    driver.get('https://www.baidu.com')
    time.sleep(5)
