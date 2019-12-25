# -*- coding: utf-8 -*-

from HtscUtils.SpiderUtils.ChromeDriver import HTChromDriver, Excon, BY

"""
浏览器调用示例
1. 模拟登陆示例：
test_login()
2. 等待页面元素加载示例：
test_wait()
3. iframe切换示例：
test_iframe()
"""


def test_login():
    login_dict = {
        'SciName': 'huatai68',
        'SciPwd': 'lhzq06',
        'Btn_Login': 1
    }
    # d = HTChromDriver(url='http://price.sci99.com/register.aspx', selector='id', login_info=login_dict)
    # d.send()
    # d.click()
    # print(d.cookies)
    # d.driver.quit()
    with HTChromDriver(url='http://price.sci99.com/register.aspx', selector='id', login_info=login_dict) as htdriver:
        htdriver.send()
        htdriver.click()
        print(htdriver.cookies)


def test_wait():
    # //div[@id='breadcrumbNav']
    with HTChromDriver(url='https://home.komatsu/en/ir/demand-orders/', wait=5) as driver:
        # by = BY(selector='xpath', lan="//div[@id='breadcrumbNav']").by
        # ec = Excon(by).located
        by = BY(selector='xpath', lan="//li[@class='gdprBtn']").by
        ec = Excon(by).clickable
        ret = driver.wait_until(ec)
        print(ret)
        print(driver.html)


def test_iframe():
    login_dict = {
        'chemname': 'huatai68',
        'chempwd': 'lhzq06',
        'ImageButton1': 1
    }
    # //*[@id="Panel_Login"]/iframe
    with HTChromDriver(url='http://cement.sci99.com/news/32747920.html', selector='id', login_info=login_dict)as driver:
        driver.to_iframe('//*[@id="Panel_Login"]/iframe')
        driver.send()
        driver.click()
        print(driver.cookies)


if __name__ == '__main__':
    # test_login()
    test_wait()
    # test_iframe()
