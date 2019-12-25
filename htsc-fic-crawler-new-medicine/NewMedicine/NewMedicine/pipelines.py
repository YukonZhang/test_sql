# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .ruku import Ruku


class NewmedicinePipeline(object):
    def open_spider(self, spider):
        if spider.name == 'consistent':
            self.ruku = Ruku('CRAWLER_MEDICINE_CONSISTENT')
        if spider.name == 'news':
            self.ruku = Ruku('CRAWLER_MEDICINE_NEW')
        if spider.name == 'cdt':
            self.ruku = Ruku('CRAWLER_MEDICINE_CLINICAL')

    def process_item(self, item, spider):
        if spider.name == 'consistent':
            self.ruku.add(item, 'acceptancenumber', 'medicinename')
        if spider.name == 'news':
            self.ruku.add(item, 'acceptancenumber')
        if spider.name == 'cdt':
            self.ruku.add(item, 'registnumber')
        return item

    def close_spider(self, spider):
        if spider.name == 'consistent':
            self.ruku.close()
        if spider.name == 'news':
            self.ruku.close()
        if spider.name == 'cdt':
            self.ruku.close()
