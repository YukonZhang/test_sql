# -*- coding: utf-8 -*-

import execjs
import js2py

with open('satcm.js', 'r', encoding='utf-8') as f:
    js1 = f.read()
    ecjs = execjs.compile(js1)

verify_data = ecjs.call('stringToHex', '0,0')
print(verify_data)
srcurl = ecjs.call('stringToHex', 'http://www.satcm.gov.cn/a/zcwj/')
