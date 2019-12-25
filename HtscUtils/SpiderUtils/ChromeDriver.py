# -*- coding: utf-8 -*-
# selenium模块封装
import os, sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By

"""
使用说明：
浏览器类调用方法有两种(推荐第一种)：
1.使用上下文管理器形式调用，可实现操作完毕后自动关闭杀死浏览器进程
示例 --> 
with HTChromeDriver() as my_driver:
    ...
2.直接实例化使用，操作结束需手动杀死进程 driver.quit()
示例 -->
my_driver = HTChromDriver()
...
my_driver.quit()
"""


class HTChromDriver(object):
    """
    chrome类，爬虫项目调用
    调用方式：1. HTChromeDriver() 实例化方式，同webdriver.Chrome，逻辑编写结束需按流程执行quit()方法
              2. with语句，通过上下文管理器调用，可实现浏览器进程自动退出。
                 使用示例：with HTChromeDriver() as htdriver:
    参数说明：options为自定义浏览器配置，默认为None
              wait为超时时间，默认10s
              selector为元素定位方式，默认使用xpath，也可以传'id'（根据id定位元素）
              login_info为登录信息字典参数，基本格式为{xpath语句/id：要输入的内容}，若定位元素为点击按钮则写作{xpath语句/id：1}
              示例： {
              '//div/input[@id="username"]':'username',
              '//div/input[@id="password"]':'password',
              '//div/button':1
              }
    """

    def __init__(self, url, options=None, wait=10, selector='xpath', login_info=None):
        self.options = options if options else None
        self.s_url = url
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self._wait = WebDriverWait(self.driver, timeout=wait)
        self.selector = selector
        self.enl_li = []
        if login_info:
            for i in login_info.items():
                self.enl_li.append(i)

    def __enter__(self):
        self.driver.maximize_window()
        self.driver.get(self.s_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    @property
    def html(self):
        return self.driver.page_source

    @property
    def cookies(self):
        return self.driver.get_cookies()

    @property
    def wait(self):
        return self._wait

    def send(self):
        if self.enl_li:
            for x, t in self.enl_li:
                if not t == 1:
                    if self.selector == 'xpath':
                        self.driver.find_element_by_xpath(x).send_keys(t)
                    if self.selector == 'id':
                        self.driver.find_element_by_id(x).send_keys(t)
                    else:
                        raise Exception('请使用xpath或id定位')
        else:
            raise Exception('未传入元素定位字典！')

    def click(self):
        if self.enl_li:
            for x, t in self.enl_li:
                if t == 1:
                    if self.selector == 'xpath':
                        button = self.driver.find_element_by_xpath(x)
                        button.click()
                    if self.selector == 'id':
                        button = self.driver.find_element_by_id(x)
                        button.click()
                    else:
                        raise Exception('请使用xpath或id定位')
        else:
            raise Exception('未传入元素定位字典！')

    def wait_until(self, ec):
        """
        浏览器实例wait until方法，结合BY类和Excon类使用
        通过检测某一元素是否已加载或是否可点击，判断页面是否载入完成
        避免固定的time.sleep
        :param ec: Excon类的属性
        :return:
        """
        ret = self._wait.until(ec)
        return ret

    def to_iframe(self, xpath=None, id=None, name=None, class_name=None):
        """
        切换至iframe
        :param xpath: 定位iframe的xpath语句
        :return:
        """
        if xpath:
            iframe = self.driver.find_element_by_xpath(xpath)
            self.driver.switch_to.frame(iframe)
        elif id:
            iframe = self.driver.find_element_by_id(id)
            self.driver.switch_to.frame(iframe)
        elif name:
            iframe = self.driver.find_element_by_name(name)
            self.driver.switch_to.frame(iframe)
        elif class_name:
            iframe = self.driver.find_element_by_class_name(class_name)
            self.driver.switch_to.frame(iframe)
        else:
            raise Exception('缺少定位iframe的参数！')


class BY(object):
    """
    参数说明：selector为元素定位方式，默认xpath选择器。 lan为定位语句（条件）
    目前支持四种定位元素方式：xpath -- xpath语句； css -- css选择器； id -- 元素ID； name -- class_name。
    均以字符串类型传参，不支持的方式会抛出异常
    """

    def __init__(self, selector='xpath', lan=''):
        if selector == 'xpath':
            self.locator = (By.XPATH, lan)
        elif selector == 'css':
            self.locator = (By.CSS_SELECTOR, lan)
        elif selector == 'id':
            self.locator = (By.CSS_SELECTOR, lan)
        elif selector == 'name':
            self.locator = (By.CLASS_NAME, lan)
        else:
            raise Exception('selector参数有误！')

    @property
    def by(self):
        return self.locator


class Excon(object):
    """
    属性说明：
            located -- 元素是否加载判定
            clickable -- 元素是否可点击判定
    """

    def __init__(self, by):
        self.by = by

    @property
    def located(self):
        return EC.presence_of_element_located(self.by)

    @property
    def clickable(self):
        return EC.element_to_be_clickable(self.by)


# if __name__ == '__main__':
#     with HTChromDriver() as hd:
#         hd.get('https://www.baidu.com')
#         time.sleep(2)
#         # print(hd.page_source)
#         print(hd.current_url)
