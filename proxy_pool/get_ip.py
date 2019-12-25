import requests
import json
import aiohttp
import asyncio
import time
import redis
from random import *
import requests
MAX_SOURCE = 100
MIN_SOURCE = 0
INITAL_SOURCE = 95
PROXY_KEY = 'proxies'
from lxml import etree
import time


def get_ip():
    headers = {
        'Cookie': 'channelid=0; sid=1569391944721205; _ga=GA1.2.1408972912.1569392452; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1569392452,1569566214; _gid=GA1.2.395889381.1569566214; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1569567283',
        'Referer': 'https://www.kuaidaili.com/free/inha/5/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    insert = Getter()
    for i in range(1, 10):
        time.sleep(2)
        url = 'https://www.kuaidaili.com/free/inha/%s/' % i
        reponse = requests.get(url, headers=headers).content.decode()
        reponse = etree.HTML(reponse)
        ip_list = reponse.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for ip in ip_list:
            ip_adr = ip.xpath('./td[1]/text()')[0]
            ip_port = ip.xpath('./td[2]/text()')[0]
            ip_mod = ip.xpath('./td[4]/text()')[0]
            insert.add(ip_adr + ':' + ip_port)
            print(i, ip_adr, ip_port, ip_mod)


# ip 获取模块
class Getter(object):
    def __init__(self):
        self.redis = redis.StrictRedis()

    def Get_ip(self):
        if len(self.redis.zrangebyscore(PROXY_KEY, MAX_SOURCE, MAX_SOURCE)) > 10:
            print('可用代理大于10，暂停获取')
            return
        # 快代理ip
        # try:
        #     get_ip()
        #     time.sleep(60 * 10)
        # except:
        #     time.sleep(60)
        proxy_api = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=154178c1ba12498e840d598aa1958d41&orderno=YZ201910222784IIkIaY&returnType=2&count=10'
        ip_response = requests.get(url=proxy_api)
        ip_content = ip_response.content.decode()
        ip_content = json.loads(ip_content)
        # tester = Tester()
        if ip_content['ERRORCODE'] == '0':
            print('===========IP获取成功========')
            # 循环获取已得到的ip
            for proxy in ip_content['RESULT']:
                proxy_ip = proxy['ip'] + ':' + proxy['port']
                # 存储
                self.add(proxy_ip)
                print(proxy_ip)
            # print(ip_content)
        else:
            print(ip_content["RESULT"])
        # time.sleep(60)

    def add(self, proxy, source=INITAL_SOURCE):
        '''
        添加新代理
        :param proxy:
        :return:
        '''
        if not self.redis.zscore(PROXY_KEY, proxy):
            return self.redis.zadd(PROXY_KEY, {proxy: source})

    def random(self, ):
        '''
        随机获取有效代理
        :return: 随机代理
        '''
        result = self.redis.zrangebyscore(PROXY_KEY, MAX_SOURCE, MAX_SOURCE)
        if len(result):
            return choice(result)
        else:
            result = self.redis.zrevrange(PROXY_KEY, 1, 100)
            if len(result):
                return choice(result)
            else:
                return '无有效代理'

    def decrease(self, proxy):
        '''
        代理减1分，少于0时删除代理
        :param proxy:
        :return: 修改后的代理分数
        '''
        source = self.redis.zscore(PROXY_KEY, proxy)
        if source and source > MIN_SOURCE:
            print('代理', proxy, '当前分数', source, '减1')
            return self.redis.zincrby(PROXY_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', source, '移除')
            return self.redis.zrem(PROXY_KEY, proxy)

    def count(self):
        '''
        获取代理池ip数量
        :return:
        '''
        return self.redis.zcard(PROXY_KEY)

    def counts(self):
        '''
        获取代理池ip数量
        :return:
        '''
        return len(self.redis.zrangebyscore(PROXY_KEY, MAX_SOURCE, MAX_SOURCE))


if __name__ == '__main__':
    get_ip()
