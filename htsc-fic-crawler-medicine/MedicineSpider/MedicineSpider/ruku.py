# -*- coding: utf-8 -*-
import cx_Oracle
import os
import re
import logging

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class Ruku(object):
    def __init__(self, tablename):
        self.conn = cx_Oracle.connect('crawler/crawler@168.61.2.2:1521/servdb')
        self.cur = self.conn.cursor()
        self.tablename = tablename

    def add(self, item, *args):
        '''
        :param item: 数据字典
        :param args: 去重字段
        :return: 无
        '''
        try:
            if len(args) == 0:  # 无去重字段
                return self.save(item)
            elif self.isesists(**{key: item[key] for key in args}):
                return self.save(item)
            else:
                logging.info('=========数据已存在=========')
                # print('=========数据已存在=========')
        except Exception as e:
            logging.error(e)
            # print(e)

    def save(self, item):
        keys = []  # 定义键
        values = []  # 定义值
        for key, value in item.items():
            keys.append(str(key))
            if re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(value)):
                values.append("to_date('{}','YYYY-MM-DD HH24:MI:SS')".format(str(value)))
                continue
            elif re.findall("\d{4}-\d{2}-\d{2}", str(value)):
                values.append("to_date('{}','YYYY-MM-DD')".format(str(value)))
                continue
            # if key == 'text':
            #     continue
            values.append("'" + str(value) + "'")
        keys = ','.join(keys)
        values = ','.join(values)
        # print(values)
        try:
            keys += ',ID'
            values += ",{}".format('SEQ_ID.nextval')
            sql = "insert into {}({}) values({})".format(self.tablename, keys, values)
            # print(sql)
            self.cur.execute(sql)
            self.conn.commit()
            logging.info('入库成功：{}'.format(item))
            return True
        except Exception as e:
            logging.error(e)
            self.conn.rollback()
            logging.error('入库失败：{}'.format(item))
            return False

    def update(self, item, update_keys=[], *args):
        '''
        :param item: 数据
        :param update_keys: 跟新字段
        :param args: 去重字段
        :return:
        '''
        if len(args) == 0 or not isinstance(update_keys, list) or len(update_keys) == 0:
            logging.warning('==========请检查更新字段或者去重字段格式是否正确！！！！！！========')
            return
        elif self.isesists(**{key: item[key] for key in args}):
            logging.info('======数据不存在，开始新增数据=====')
            self.save(item)
        else:
            isat_sql = []
            for key in args:
                isat_sql.append("{}='{}'".format(str(key), item[str(key)]))
            isat_sql = ' and '.join(isat_sql)
            updata_sql = []
            for key in update_keys:
                updata_sql.append("{}='{}'".format(str(key), str(item[str(key)])))
            updata_sql = ','.join(updata_sql)
            logging.info('======数据存在开始更新数据======')
            sql = "update {} set {} where {}".format(self.tablename, updata_sql, isat_sql)
            # print(sql)
            try:
                self.cur.execute(sql)
                self.conn.commit()
                print("数据更新成功")
            except:
                self.conn.rollback()
                print("数据更新失败")

    def isesists(self, **kwargs):
        '''
        :param tablename:
        :param kwargs:
        :return:
        '''
        data = []
        for key, value in kwargs.items():
            if re.findall("\d{4}-\d{2}-\d{2}", str(value)):
                value = "to_date('{}','YYYY-MM-DD')".format(str(value))
                data.append(str(key) + '=' + str(value))
                continue
            data.append(str(key) + '=' + "'" + str(value) + "'")
        data = ' and '.join(data)
        sql = "select count(id) from {} where {}".format(self.tablename, data)
        self.cur.execute(sql)
        if self.cur.fetchall()[0][0]:
            return False
        else:
            return True

    def close(self):
        self.cur.close()
        self.conn.close()

# if __name__ == '__main__':
#     test = Ruku('EDB_ZCINDUSTRYINDEXDATA')
#     test.add(
#         {'remark': '', 'minvalue': 389, 'maxvalue': 389, 'pubdate': '2019-10-24', 'value': 389.230774,
#          'indexid': 'B3EF0F12-9FE3-46D2-88BA-026DF0D8E602',
#          'isvalid': 1, 'entyrtime': '2019-11-05 10:10:10', 'updatetime': '2019-11-05 10:10:10', 'groundtime': '2019-11-05 10:10:10',
#          'resourceid': '爬虫', 'recordid': '原始数据拉取接口'}, 'pubdate', 'indexid')
