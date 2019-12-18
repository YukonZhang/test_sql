# -*- coding: utf-8 -*-

import requests
from requests.sessions import Session
from HtscUtils.SpiderUtils.BrowserUA import BrowserUA

start_url = 'http://www.cde.org.cn/news.do?method=news_index_yzxpj'

l_url = 'http://www.cde.org.cn/yzxpjNotice.do?method=yzxpjNoticeList'

headers = {
    'Host': 'www.cde.org.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.cde.org.cn/yzxpjNotice.do?method=yzxpjNoticeList',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'FSSBBIl1UgzbN7N80S=wn623zSQU.WxQ714ZPUuGAfVwHzTTTVOfw4_.R.btV0ec0_hYWQxOkmUu7cmGPr.; JSESSIONID=0001DHvi6hyBif94P7qOqaUrj4X:-4LHIBT; FSSBBIl1UgzbN7N80T=3VrZ1hgTK2hEEbkmxVieHqMdsC09Ir4hxvDtt2nrLjessOYkjx63Ua1n.cnXTmw5ehOtKTYNLIb7Ai3akdF.7bBY.WdZD1VbmVNlmxlk5T1DxWzbxYOOQoWTTKpW.49UFYkNHm_J4l8.oArDvWqdcRJ3zJm8G4fkAqdB3pgMIKgv8TDx3hc9KF0dcg9V4LiRfJ5KR4RK5n2G634c.eck7Zn7gLgbDBsbCltUJFcI5OKPQsj1YfRo05bBarxgwShojwvCykWHeMYJRDWT_xSwVXGORAWD_SYybV.BVPJZqja7yok4AN13_q.FX4L2j.1q9YsCOFIHTyS6B9C9zs0wjshjZnOIp1bBKJObqFwhupI8iWA; td_cookie=2750548012'
}

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#     # 'Referer': l_url,
#     # 'Cookie':'FSSBBIl1UgzbN7N80S=wn623zSQU.WxQ714ZPUuGAfVwHzTTTVOfw4_.R.btV0ec0_hYWQxOkmUu7cmGPr.; JSESSIONID=0001DHvi6hyBif94P7qOqaUrj4X:-4LHIBT; td_cookie=2750548012; FSSBBIl1UgzbN7N80T=3_jKL2sI7hGPnELBu_2UTXaYN3Ii2BAfuxzGahR.1lKyNJ5NAvQnz8y3p7RlH.CVo2EG7M5k1SJDjGuFypSrKEldpLIvslVoyvvw96J0xI9xlzzuG1sCyX6HiEm7vucz1pWeN.89KPHDL6o.XjQ_J2c002k10vzdBGKv1DzXtTNbKrm3uMBndrYIQmT1LDSgXx5EOeV2vXLarlSs8F.tRMJpqforHnfYg6fG0M8BEBPRHrl6x2llkuE9DE3Ccq5yyIG1yzYOsFs.4VzG6p_XSaMGCeVrPEO26Fl7mjhggKZerhYJNSDCvlobxAKNoUPYpNN9R.7co5Wj9Pg5wYX5yTV2P4eICB4jQnBV2A8Q3LebgBA'
# }
sess = Session()
ret = sess.get(start_url, headers=headers)
resp = sess.get(l_url, headers=headers)

print(resp.content.decode('utf-8'))
