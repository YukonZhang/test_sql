# -*- coding: utf-8 -*-
import cx_Oracle
import os
import re

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
                self.save(item)
            elif self.isesists(**{key: item[key] for key in args}):
                self.save(item)
            else:
                print('=========数据已存在=========')
        except Exception as e:
            print(e)

    def save(self, item):
        keys = []  # 定义键
        values = []  # 定义值
        for key, value in item.items():
            keys.append(str(key))
            ############################################################################################
            # 针对时间格式所做的修改，暂无时间格式，代码注释
            if re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(value)):
                values.append("to_date('{}','YYYY-MM-DD HH24:MI:SS')".format(str(value)))
                continue
            if re.findall("\d{4}-\d{2}-\d{2}", str(value)):
                values.append("to_date('{}','YYYY-MM-DD')".format(str(value)))
                continue
            #############################################################################################
            values.append("'" + str(value) + "'")
        keys = ','.join(keys)
        values = ','.join(values)

        # print(values)
        # exit()
        try:
            keys += ',ID'
            values += ",{}".format('SEQ_ID.nextval')
            sql = "insert into {}({}) values({})".format(self.tablename, keys, values)
            # print(sql)
            self.cur.execute(sql)
            self.conn.commit()
            print('入库成功：{}'.format(item))
        except Exception as e:
            print(e)
            self.conn.rollback()
            print('入库失败：{}'.format(item))

    def update(self, item, update_keys=[], *args):
        '''
        :param item: 数据
        :param update_keys: 跟新字段
        :param args: 去重字段
        :return:
        '''
        if len(args) == 0 or not isinstance(update_keys, list) or len(update_keys) == 0:
            print('==========请检查更新字段或者去重字段格式是否正确！！！！！！========')
            return
        elif self.isesists(**{key: item[key] for key in args}):
            print('======数据不存在，开始新增数据=====')
            self.save(item)
        else:
            isat_sql = []
            for key in args:
                #######################################################################################################
                # 针对时间格式所做的修改，暂无时间格式，代码注释
                if re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(item[str(key)])):
                    isat_sql.append(
                        str(key) + '=' + "to_date('{}','YYYY-MM-DD HH24:MI:SS')".format(str(item[str(key)])))
                    continue
                if re.findall("\d{4}-\d{2}-\d{2}", str(item[str(key)])):
                    isat_sql.append(str(key) + '=' + "to_date('{}','YYYY-MM-DD')".format(str(item[str(key)])))
                    continue
                #######################################################################################################
                isat_sql.append("{}='{}'".format(str(key), item[str(key)]))
            isat_sql = ' and '.join(isat_sql)
            updata_sql = []
            for key in update_keys:
                updata_sql.append("{}='{}'".format(str(key), str(item[str(key)])))
            updata_sql = ','.join(updata_sql)
            print('数据存在开始更新数据')
            sql = "update {} set {} where {}".format(self.tablename, updata_sql, isat_sql)
            print(sql)
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
            #######################################################################################################
            # 针对时间格式所做的修改，暂无时间格式，代码注释
            if re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(value)):
                data.append(str(key) + '=' + "to_date('{}','YYYY-MM-DD HH24:MI:SS')".format(str(value)))
                continue
            if re.findall("\d{4}-\d{2}-\d{2}", str(value)):
                data.append(str(key) + '=' + "to_date('{}','YYYY-MM-DD')".format(str(value)))
                continue
            #######################################################################################################
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


if __name__ == '__main__':
    test = Ruku('BUILDING_INFO')
    test.add(
        {'dataname': '水泥价格:华北:天津:P.O42.5', 'datvalue': 380, 'pubdate': '2012-01-12 00:00:00', 'unit': '元/吨',
         'frequency': '周',
         'resouse': 'excel解析', 'fmenu': '水泥价格'})
