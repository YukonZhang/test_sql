# -*- coding: utf-8 -*-

import requests
from proxies import ip_redis

ip = ip_redis().random()
proxies = {'http': ip}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': 'security_session_verify=30ed67f1bf89183c6792a16e64a0ea88; srcurl=687474703a2f2f7777772e736174636d2e676f762e636e2f612f7a63776a2f; security_session_mid_verify=0c1ba526a7cd0f564ccf4e1bcb155a6c',
    'Host': 'www.satcm.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.satcm.gov.cn/a/zcwj/?security_verify_data=313533362c383634',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
resp = requests.get('http://www.satcm.gov.cn/a/zcwj/', headers=headers, proxies=proxies)
print(resp.content.decode())
