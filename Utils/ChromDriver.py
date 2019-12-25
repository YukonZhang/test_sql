# -*- coding: utf-8 -*-
# selenium模块封装

from selenium import webdriver


class HTChromDriver(object):
    def __init__(self, options=None):
        self.options = options if options else None
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def __enter__(self):
        self.driver.maximize_window()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


if __name__ == '__main__':
    with HTChromDriver() as hd:
        hd.get('https://www.baidu.com')
        print(hd.page_source)
        print(hd.current_url)

