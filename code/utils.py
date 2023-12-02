'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC else001@sina.com
LastEditors: WT-H-PC else001@sina.com
LastEditTime: 2023-12-01 23:01:44
Description: tool class and tool functions
'''


import logging
import time
import random

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 打印函数的出入口,@assistant相当于先初始化,初始化函数也会调用__call__,然后再调用assistant(func)
# 装饰器不带括号，原函数直接作为参数传给装饰器，类似desc(func)
# 装饰器带括号，相当于装饰器的方法dec先执行，dec()运行后返回一个内层的函数inner_desc， 由这个inner_desc作为装饰器，原函数实际是传给inner_desc，等价于inner_desc(f)
# 装饰器类
class assistant():
    # 装饰器使用时必须要带括号，因为这个要先执行这个函数
    def __init__(self, level='INFO'):
        self.level = level
        
    # 被装饰的函数执行时，先进入装饰器
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            log_msg = f'function[{func.__qualname__}] begins............'
            self.__log(log_msg)
            
            res = func(*args, **kwargs)
            
            log_msg = f'function[{func.__qualname__}] ends............\n'
            self.__log(log_msg)
            return res
        return wrapper


    def __log(self, msg):
        if self.level == 'DEBUG':
            logging.debug(msg)
        elif self.level == 'ERROR':
            logging.error(msg)
        else:
            logging.info(msg)


# 获取本地时间，格式为YYYY-mm-DD HH:MM:SS
def getlocaltime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 随机暂停一段时间，单位为秒
def pause(start=1, end=3):
    tick = random.uniform(start, end)
    time.sleep(tick)
    return tick