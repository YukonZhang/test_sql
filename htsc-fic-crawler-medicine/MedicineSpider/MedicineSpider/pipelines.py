# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .ruku import Ruku


class MedicinespiderPipeline(object):
    def open_spider(self, spider):
        if spider.name in ['nhsa', 'nhc', 'nmpa']:
            self.ruku_main = Ruku('CRAWLER_MEDICINEPOLICY')
            self.ruku_ass = Ruku('CRAWLER_MEDICINEPOLICY_LINK')

    def close_spider(self, spider):
        if spider.name in ['nhsa', 'nhc', 'nmpa']:
            self.ruku_ass.close()
            self.ruku_main.close()

    def process_item(self, item, spider):
        if spider.name in ['nhsa', 'nhc', 'nmpa']:
            item_main = item['main']
            r = self.ruku_main.add(item_main, 'policyid')
            if r:
                ass_li = item['ass']
                for item_ass in ass_li:
                    self.ruku_ass.add(item_ass, 'policyid', 'annexname')
        return item
