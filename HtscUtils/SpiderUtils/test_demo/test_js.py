# -*- coding: utf-8 -*-

from HtscUtils.SpiderUtils.DealJS import DealJS


def main1():
    """
    调用简单的js语句
    :return:
    """
    dj = DealJS('var a="hello"')
    ret = dj.exec_str()
    print(ret)


def main2():
    """
    调用js函数
    :return:
    """
    js_str = """
    function add(a, b)
    {
    return a+b
    }
    """
    dj = DealJS(js_str=js_str)
    ret = dj.exec_func(2, 3)
    print(ret)


def main3():
    """
    读取js文件并执行
    :return:
    """
    dj = DealJS(path='../js_file/test.js')
    ret = dj.exec_file()
    print(ret.guid1)


if __name__ == '__main__':
    main1()
    main2()
    main3()
