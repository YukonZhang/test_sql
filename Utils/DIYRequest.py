# -*- coding: utf-8 -*-
# 自定义request对象

import requests
from requests.sessions import Session
from scrapy.http.request import Request


class DiyRequest(Request):
    # TODO
    def get_session(self):
        pass
