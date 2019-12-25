import json
import aiohttp
import asyncio
import time
import redis

BATCH_TEST_SIZE = 100
from proxy_pool.get_ip import *


# ip 检测
class Tester(object):
    def __init__(self):
        self.redis = redis.StrictRedis()

    async def test_single_proxy(self, proxy):
        '''
        测试代理ip
        :param proxy: 单个代理
        :return:
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            rel_proxy = 'http://' + proxy
            try:
                print('正在测试：', proxy)
                async with session.get(
                        'https://www.baidu.com/',
                        proxy=rel_proxy, timeout=10) as response:
                    if response.status == 200:
                        print('代理可用：', proxy)
                        self.max(proxy)
                    else:
                        print('代理不可用：', proxy)
                        self.decrease(proxy)
            except:
                self.decrease(proxy)
                print('代理请求失败')

    def max(self, proxy):
        '''
        将代理设为最大值
        :param proxy:
        :return:
        '''
        print('代理', proxy, '可用，设置为', MAX_SOURCE)
        return self.redis.zadd(PROXY_KEY, {proxy: MAX_SOURCE})

    def decrease(self, proxy):
        '''
        代理减1分，少于0时删除代理
        :param proxy:
        :return: 修改后的代理分数
        '''
        source = self.redis.zscore(PROXY_KEY, proxy)
        if source and source > MIN_SOURCE:
            print('代理', proxy, '当前分数', source, '减10')
            return self.redis.zincrby(PROXY_KEY, -10, proxy)
        else:
            print('代理', proxy, '当前分数', source, '移除')
            return self.redis.zrem(PROXY_KEY, proxy)

    def run(self):
        '''
        测试主函数
        :return: None
        '''
        print('===========测试器开始运行===========')
        try:
            # 获取所有代理
            proxies = self.redis.zrangebyscore(PROXY_KEY, MIN_SOURCE, MAX_SOURCE)
            proxies = [i.decode() for i in proxies]
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i + BATCH_TEST_SIZE]
                task = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(task))
                time.sleep(1)
        except:
            print('===========测试器发生错误==========')


if __name__ == '__main__':
    Tester().run()
