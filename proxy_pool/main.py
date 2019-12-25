import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from proxy_pool.app import *
from proxy_pool.tester import *
from multiprocessing import Process
class Scheduler():
    def schedule_tester(self, cycle=20):
        '''
        定时测试代理
        :param cycle: 定时时间
        :return:
        '''
        testr = Tester()
        while True:
            print('==============测试代理开始运行==============')
            testr.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=20):
        '''
        定时获取代理
        :param cycle:
        :return:
        '''
        getter = Getter()
        while True:
            print('==============开始抓取代理=============')
            getter.Get_ip()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启api
        :return:
        '''
        app.run('127.0.0.1', '8000')

    def run(self):
        print('========代理池开始运行========')
        tester_process = Process(target=self.schedule_tester)
        tester_process.start()
        getter_process = Process(target=self.schedule_getter)
        getter_process.start()
        api_process = Process(target=self.schedule_api)
        api_process.start()


if __name__ == '__main__':
    Scheduler().run()
