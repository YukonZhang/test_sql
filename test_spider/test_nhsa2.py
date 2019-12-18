# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re

headers = {
    'Cookies': 'td_cookie=3189545171; FSSBBIl1UgzbN7N80S=O.Jim4JWJ73pvQfXDd.Ybr2KsvBxmerAQ1dwH6ay7MzbBpPKeKIeeVlgK5B2WI3a; banggoo.nuva.cookie=6|Xe3z1|Xe3z1; FSSBBIl1UgzbN7N80T=3b7bVFTFzDsoUhNLx4r8e2.hxaps32atStqMS.wZ0AcKso.0koxaDXO.RMxBbBR5Z7KHshHcADGIYVcBFnCbfxP2LpCwGPV6idZEwKL3BjjrvZZw.jkMdyNO27XU70qV8A4vxYIi8OrCSZozdhG30JjHimU3nayshIgfucyRhSAFcELGZ6JN0qTaWq6a8R5H4O_TA5a.KnS2zXtYdoKyOFUU_hiEp68osnsiEMcDas3WYu5BzqN4LOOnnvg_.V8wcTnBIzvz0ZZmG_D95NJWpGuxb4nMML1SEb.faSqEBK16v0bMEJrUEDxZlW64wd5t8ujbSoONO5j2Esy9UrGd.3ev69O83FdgGvcLKTinNoGv6lmC3N2lJ3Jxwiqop.i2otX7'
}
sess = requests.Session()
a = sess.get('http://www.nhc.gov.cn/wjw/zcfg/list.shtml')
print(a.status_code)
b = sess.get('http://www.nhc.gov.cn/wjw/zcfg/list.shtml')
print(b.status_code)
resp = sess.get('http://www.nhc.gov.cn/wjw/zcfg/list.shtml')
print(resp.status_code)
# # # print(resp.status_code)
# # # print(resp.content.decode('utf-8'))
# # response = etree.HTML(resp.content.decode('utf-8'))
# # text_div = response.xpath('//div[@id="zoom"]//text()')
# # # text = ' '.join(text_div.xpath('.//text()').extract()).strip()
# # # t = text_div.xpath('.//text()')
# # print(text_div)
#
with open('a.html', 'w')as f:
    f.write(resp.content.decode('utf-8'))

# u = ' http://www.nhc.gov.cn/wjw/zcjd/201304/a3a628c1c85e4b3ebda02f07f7de4fd5.shtml'
# resp = requests.get(u)
# ret = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', resp.text)[0]
# print(ret)
