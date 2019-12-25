# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *  # 区分大小写
from sqlalchemy.orm import sessionmaker


class Mobile():
    '''
    自定义入库字段
    '''
    id = Column(Integer, primary_key=True, comment='ID')
    fmenu = Column(String(50), comment='一级菜单')
    dataname = Column(String(50), comment='指标名称')
    min_price = Column(String(50), comment='最低价')
    arg_price = Column(String(50), comment='平均价')
    max_price = Column(String(50), comment='最高价')
    datvalue = Column(String(50), comment='指标值')
    unit = Column(String(50), comment='单位')
    frequency = Column(String(50), comment='更新频率')
    pubdate = Column(String(50), comment='发布时间')
    entrytime = Column(DateTime, server_default=func.now(), comment='创建时间')
    resouse = Column(String(50), comment='数据来源')

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class Ruku(object):
    def __init__(self, table_name='building_info'):
        '''
        :param table_name:数据库表明，每次新建表时修改
        '''
        self.engine = create_engine('oracle://crawler:crawler@168.61.2.2:1521/SERVDB', echo=True)  # 连接数据库
        self.session = sessionmaker(bind=self.engine)
        self.sess = self.session()
        self.Base = declarative_base()
        # 动态创建orm类,必须继承Base, 这个表名是固定的,如果需要为每个爬虫创建一个表,请使用process_item中的
        self.Mob = type(table_name, (self.Base, Mobile), {'__tablename__': table_name})
        # 判断数据表是否存在 如果没有自动创建
        if 'building_info' not in self.engine.table_names():  # create table for this spider
            self.Mob.metadata.create_all(self.engine)

    #  去重操作
    def Quchong(self, item):
        isexist = self.sess.query(self.Mob).filter_by(dataname=item['dataname'],
                                                      pubdate=item['pubdate']).first()
        if isexist:  # 为真数据存在
            return False
        else:
            return True

    # 入库操作
    def Ruk(self, item):
        if self.Quchong(item):
            self.sess.add(self.Mob(**item))
            self.sess.commit()
            print('入库成功：', item)
        else:
            print('======数据以存在，入库失败======')

    # 数据更新专用
    def updated(self, item):
        isexist = self.sess.query(self.Mob).filter_by(dataname=item['dataname'],
                                                      pubdate=item['pubdate']).first()
        if isexist:  # 为真数据存在
            isexist.datvalue = item['datvalue']
            print('===========数据更新成功========')
        else:
            self.sess.add(self.Mob(**item))
        self.sess.commit()

    # todo:关闭会话
    def Close(self):
        self.session.close_all()
