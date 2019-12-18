# -*- coding: utf-8 -*-
import requests
from lxml import etree

form_data = {
    'col': 1,
    'appid': 1,
    'webid': 1,
    'path': '/',
    'columnid': 37,
    'sourceContentType': 1,
    'unitid': 753,
    'webname': '国家医疗保障局',
    'permissiontype': 0
}
p_url = 'http://www.nhsa.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=1000&perpage=1000'
jd_url = ''

resp = requests.post(p_url, data=form_data)
ret = resp.content.decode('utf-8')

tree = etree.HTML(ret)
r_li = tree.xpath('//recordset/record//a/@href')
print(r_li)


# http://www.nhsa.gov.cn/col/col37/index.html