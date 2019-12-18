# -*- coding: utf-8 -*-
import requests
import json
import redis
import time


class ip_redis():
    def __init__(self):
        self.redis = redis.StrictRedis()

    def get_ip(self):
        # print('开始获取ip')
        IP = requests.get(
            'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=780f2d80758044d19d219f95e2a85d75&orderno=YZ201910173971UbUNv8&returnType=2&count=10')
        IP = json.loads(IP.content.decode())
        if IP['ERRORCODE'] != '0':
            time.sleep(2)
            self.get_ip()
        else:
            for ip in IP['RESULT']:
                proxy = 'http://' + ip['ip'] + ':' + ip['port']
                self.add(proxy)

    def add(self, ip):
        self.redis.sadd('proxy_set', ip)

    def del_ip(self, ip):
        '''
        删除ip
        :param ip:
        :return:
        '''
        # print('删除ip：{}'.format(ip))
        self.redis.srem('proxy_set', ip)

    def random(self):
        '''
        获取随机ip
        :return:
        '''
        if self.redis.scard('proxy_set') < 5:
            self.get_ip()
        ip = self.redis.srandmember('proxy_set').decode()
        is_ues = self.tester(ip)
        if is_ues:
            return is_ues
        else:
            self.del_ip(ip)
            return self.random()

    def tester(self, ip):
        try:
            tester = requests.get('http://www.baidu.com', proxies={'http': ip}, timeout=3)
            if tester.status_code == 200:
                # print('ip可用')
                return ip
        except:
            # print('ip不可用')
            return False


if __name__ == '__main__':
    print(ip_redis().random())
