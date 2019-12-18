# -*- coding: utf-8 -*-
import time

import requests
from selenium.webdriver import Chrome
import execjs
from lxml import etree

# driver = Chrome()
u = 'http://www.nmpa.gov.cn/WS04/CL2170/'
u2 = 'http://www.nmpa.gov.cn/WS04/CL2196/371930.html'
#
# driver.get(u)
# driver.maximize_window()
# time.sleep(2)
# cookies = driver.get_cookies()
# # print(cookies)
# driver.quit()
# c = ''
# for k, v in cookies[0].items():
#     c += str(k) + '=' + str(v) + ';'
#
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache - Control": "max - age = 0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "app1.sfda.gov.cn",
            "Referer": "http: // app1.sfda.gov.cn / datasearchcnda / face3 / base.jsp?tableId = 28 & tableName = TABLE28 & title = % BB % A5 % C1 % AA % CD % F8 % D2 % A9 % C6 % B7 % D0 % C5 % CF % A2 % B7 % FE % CE % F1 & bcId = 152912030752488832300204864740",
            "Upgrade - Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }
# headers['cookies'] = c

# sess = requests.Session()
# r = sess.get(u)
# print(r.cookies)
# print(r.status_code)
resp = requests.get(u)
tree = etree.HTML(resp.text)
meta = tree.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
print(resp.cookies)
print(meta)
# print(r.status_code)




# print(resp.status_code)
# print(resp.text)

# cookies
# td_cookie=3431013327;
# FSSBBIl1UgzbN7N80S=vzWjnCVwuqp2Y2MFFZwlrHiH12VuWh5z9LWDfnWJcSLy.ENqDIqSrz1W3IElzBig; _
# gscu_515232071=759566235y9g1717;
# _gscbrs_515232071=1;
# _gscs_515232071=t76116503s57ady17|pv:1;
# FSSBBIl1UgzbN7N80T=2Ny4KkHAWy0k0t0sJG1G7t_SZCbyP984jTNDWD1Hnt_pSo0Se2nhyEet5yi7O.DwmQlnm_nMsBHfRqHnLIowo.lDAbDczGWwjVqmCLdp1ZYCcGWFcrDYoX1LeDoSfOy4C0NQsZumI2ZWIw9.RWWQsYjj1W7NMc5bfJb7j73rSi7Sq8MaBN58951t.jC_cZxImGLdmGUU0wMCWDmP7TCQp0MNjnWyS6iZuUWJI26xnpfZhrXC3H7SU1ueZbo43mqPWiOkpxylxq6TlrTUfNmGXC2vcXfE4yUXqYJ9.GkT2gvfJFFFRM7Y5y40RcM3U2Z6zCSW
