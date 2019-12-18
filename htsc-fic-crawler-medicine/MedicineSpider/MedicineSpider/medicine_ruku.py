# -*- coding: utf-8 -*-
import cx_Oracle
import logging
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def add(item):
    conn = cx_Oracle.connect('crawler/crawler@168.61.2.2:1521/servdb')
    cursor = conn.cursor()
    item_main = item['main']
    item_ass = item['ass']
    sql = """
                insert into CRAWLER_MEDICINEPOLICY(id, policyid, pubtime, title, policybodyurl, isvalid) 
                values (SEQ_ID.nextval, :policyid, to_date(:pubtime,'YYYY-MM-DD'), :title, :policybodyurl, :isvalid)
            """
    sql2 = """
                insert into CRAWLER_MEDICINEPOLICY_LINK(id, policyid) values (SEQ_ID.nextval, :pid)
        """
    try:
        cursor.execute(sql,
                       [item_main['policyid'], item_main['pubtime'], item_main['title'], item_main['policybodyurl'],
                        item_main['isvalid']])
        cursor.execute(sql2, [item_ass['policyid']])
        conn.commit()
        logging.info('入库成功：{}')
    except Exception as e:
        logging.error(e)
        conn.rollback()
        logging.error('入库失败：{}')
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    pass
    # conn = cx_Oracle.connect('crawler/crawler@168.61.2.2:1521/servdb')
    # cursor = conn.cursor()
    # id = "SEQ_ID.nextval"
    # sql = """
    #         insert into CRAWLER_MEDICINEPOLICY(id, policyid, pubtime, title, policybodyurl, isvalid)
    #         values (SEQ_ID.nextval, :policyid, to_date(:pubtime,'YYYY-MM-DD'), :title, :policybodyurl, :isvalid)
    #     """
    # sql2 = """
    #         insert into CRAWLER_MEDICINEPOLICY_LINK(id, policyid) values (SEQ_ID.nextval, :pid)
    # """
    # try:
    #     cursor.execute(sql,
    #                    ['124', "2019-11-02", '标题', 'http://aa', 1])
    #     cursor.execute(sql2, ['124'])
    #     conn.commit()
    #     logging.info('入库成功：{}')
    # except Exception as e:
    #     logging.error(e)
    #     conn.rollback()
    #     logging.error('入库失败：{}')
    # finally:
    #     cursor.close()
    #     conn.close()
