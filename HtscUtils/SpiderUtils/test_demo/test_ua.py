# -*- coding: utf-8 -*-

from HtscUtils.SpiderUtils.BrowserUA import BrowserUA

if __name__ == '__main__':
    bu = BrowserUA()
    print(bu.user_agent)  # 随机获取ua
    print(bu.firefox)  # 获取Firefox随机版本ua
    print(bu.chrome)  # 获取Chrome随机版本ua
    print(bu.ie)  # 获取ie随机版本ua
