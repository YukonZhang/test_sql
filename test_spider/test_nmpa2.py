# -*- coding: utf-8 -*-

import requests

u = 'http://www.nmpa.gov.cn/WS04/CL2201/357716.html'

resp = requests.get(u)

print(resp.status_code)