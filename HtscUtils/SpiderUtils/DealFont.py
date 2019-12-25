# -*- coding: utf-8 -*-
# 字体文件解析模块

from fontTools.ttLib import TTFont

"""
使用说明：
1. 字体文件处理类DealFont接受两个参数：path为字体文件路径（推荐使用绝对路径）；
texts为list类型对象，其中元素为解析工具解析出来的真实字符（按顺序放入列表）,可以传一个空列表[]。
2. 常用属性：FontDict --> 返回解密后的加密字符和真实字符的对应关系，如 '&#xf8fd': '弄'
3. 其他属性：BestCmap --> 字体编码与name的对应关系
             GlyphOrder --> GlyphID列表，元素数目即为加密字体数目
4. 方法：save_as_xml --> 将字体文件解析并写入xml，字体文件无法用编辑工具直接打开，转换成xml文件便于直观展示
    如遇到动态字体加密，可使用该方法生成xml文件，从xml中提取字符坐标以供后续图片分析进行解密。
"""


class DealFont(object):
    def __init__(self, path, texts):
        self.path = path
        self.texts = texts
        self.font = TTFont(path)
        self.name_map = {}
        self.fontmap = {}

    @property
    def BestCmap(self):
        """
        字体编码与name的对应关系
        :return:
        """
        return self.font.getBestCmap()

    @property
    def GlyphOrder(self):
        """
        GlyphID列表，元素数目即为加密字体数目
        :return:
        """
        return self.font.getGlyphOrder()

    def _get_fontmap(self):
        """
        内部处理方法，整合GlyphOrder和texts，返回加密字符与真实字符对应关系
        :return:
        """
        font_names = self.GlyphOrder
        for index, value in enumerate(self.texts):
            self.name_map[font_names[index]] = value
        for k, v in self.name_map.items():
            if k.startswith('uni'):
                key_ = k.replace('uni', '&#x')
                self.fontmap[key_] = v
            else:
                self.fontmap[k] = v
        return self.fontmap

    @property
    def FontDict(self):
        """
        该属性为字典。key为网页源码中被加密的字符，值为每个加密字符所对应的字符
        :return: font_dict
        """
        font_dict = self._get_fontmap()
        return font_dict

    def save_as_xml(self, filepath):
        """
        将字体文件解析结果保存为xml文件
        :param filepath: xml文件保存路径，推荐写绝对路径
        :return:
        """
        self.font.saveXML(filepath)
