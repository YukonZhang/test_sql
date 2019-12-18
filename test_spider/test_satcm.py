# -*- coding: utf-8 -*-

import requests
from proxies import ip_redis
import execjs
import re

url = 'http://www.satcm.gov.cn/a/zcwj/'
# u1 = 'http://fjs.satcm.gov.cn/zhengcewenjian/2018-03-24/2413.html'

# resp = requests.get(url)
# print(resp.content.decode('utf-8'))
sess = requests.Session()
ua = BrowserUA().ie
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
    'Cache-Control': 'no-cache',
    'Cookie': '',
    'Host': 'www.satcm.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': '',
    'Upgrade-Insecure-Requests': '1'
}
ip = ip_redis().random()
proxies = {'http': ip}

resp = requests.get(url, headers=headers, proxies=proxies)
# 第一个cookie字段
security_session_verify = resp.cookies['security_session_verify']
print(security_session_verify)

with open('satcm.js', 'r', encoding='utf-8') as f:
    js1 = f.read()
    ecjs = execjs.compile(js1)
# 第二个cookie字段
srcurl = ecjs.call('stringToHex', url)
print(srcurl)

verify_data = ecjs.call('stringToHex', '1536,864')
mid_url = url + '?security_verify_data=' + verify_data

headers['Referer'] = url
headers['Cookie'] = 'srcurl=' + srcurl + ';' \
                    + 'security_session_verify=' + security_session_verify
# headers['Upgrade-Insecure-Requests'] = '1'
# print(mid_url)
r = requests.get(mid_url, headers=headers, proxies=proxies)
# print(r.content.decode())
# 第三个cookie字段
security_session_mid_verify = r.cookies['security_session_mid_verify']
print(security_session_mid_verify)

s = """td_cookie=3881121226; Hm_lvt_94feb70aad10060f0d7f8d38372b1d72=1576569284; Hm_lpvt_94feb70aad10060f0d7f8d38372b1d72=1576569828;"""
headers['Cookie'] = 'security_session_verify=' + security_session_verify + ';' \
                    + 'srcurl=' + srcurl + ';' \
                    + 'security_session_mid_verify' + security_session_mid_verify

# ret = requests.get(url, headers=headers, proxies=proxies)
# # 第四个cookie字段
# td_cookie = re.findall(r'supFlash\("(\d*)"\)', ret.content.decode())[0]
# print(td_cookie)
# headers['Cookie'] = 'td_cookie=' + td_cookie + ';' + headers['Cookie']
# print(headers)
# sess.get(url, headers=headers, proxies=proxies)

headers['Referer'] = mid_url
response = requests.get(url, headers=headers, proxies=proxies)
print(response.status_code)
print(headers)
print(response.content.decode())
with open('r.html', 'w')as f:
    f.write(response.content.decode())
# print(dict(response.cookies))

# sess.get(url, headers=headers, proxies=proxies)
# sess.get(url, headers=headers, proxies=proxies)
# r = sess.get(url, headers=headers, proxies=proxies)
# print(r.content.decode('utf-8'))

# 97d26b144620c506425770a182ae5880
# 5b71da75cd78a8330cd1731755d52d09
# 113aa60155fca574addb6cff8f2d8ac4
# 810f4b95034e7aadb1be90f4da2d253a
"""
http://www.satcm.gov.cn/a/zcwj/
Set-Cookie: security_session_verify=810f4b95034e7aadb1be90f4da2d253a; expires=Sat, 21-Dec-19 09:53:35 GMT; path=/; HttpOnly
Set-Cookie: security_session_verify=810f4b95034e7aadb1be90f4da2d253a; expires=Sat, 21-Dec-19 09:53:35 GMT; path=/; HttpOnly

http://www.satcm.gov.cn/a/zcwj/?security_verify_data=313533362c383634
Set-Cookie: security_session_mid_verify=d0e7550edf48c0e60ef21ac2a2093793; expires=Sat, 21-Dec-19 09:53:43 GMT; path=/; HttpOnly
Set-Cookie: security_session_mid_verify=d0e7550edf48c0e60ef21ac2a2093793; expires=Sat, 21-Dec-19 09:53:43 GMT; path=/; HttpOnly

http://www.satcm.gov.cn/a/zcwj/
Cookie: td_cookie=3881121226; 
        Hm_lvt_94feb70aad10060f0d7f8d38372b1d72=1576569284; 
        Hm_lpvt_94feb70aad10060f0d7f8d38372b1d72=1576569828; 
        srcurl=687474703a2f2f7777772e736174636d2e676f762e636e2f612f7a63776a2f; 
        security_session_verify=810f4b95034e7aadb1be90f4da2d253a; 
        security_session_mid_verify=d0e7550edf48c0e60ef21ac2a2093793
Referer: http://www.satcm.gov.cn/a/zcwj/?security_verify_data=313533362c383634
"""
