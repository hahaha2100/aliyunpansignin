'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC else001@sina.com
LastEditors: WT-W-PC else001@sina.com
LastEditTime: 2023-12-01 13:57:44
Description: 
对http请求的各类方法进行封装,对系统、网络、客户端和服务器的错误进行捕捉，增强网络请求的健壮性。
不处理业务响应码
'''
import requests
from requests import session
import random
import logging
from utils import assistant
import utils

# 对http请求进行封装，构建底层稳定的网络层收发器，不处理业务响应码
class ReqRobot:
    def __init__(self, retries=20):
        self._log = logging
        self._session = requests.session()
        self._session.keep_alive = False
        self._headers = ReqRobot.getheaders()
        self._max_retries = retries

    def setheaders(self, headers):
        self._headers = headers

    # 封装Get方法
    @assistant('DEBUG')
    def reqget(self, url):
       return self.__reqrequest(url, 'get')

    # 封装Post方法
    @assistant('DEBUG')
    def reqpost(self, url, form_data):
        return self.__reqrequest(url, 'post', form_data)
    
    # 封装Put方法
    @assistant('DEBUG')
    def reqput(self, url, form_data=None):
        return self.__reqrequest(url, 'put', form_data)
    
    # 封装网络请求，具备失败后多次尝试的能力
    @assistant('DEBUG')
    def __reqrequest(self, url, method, form_data=None):
        result = False
        for num in range(1, self._max_retries + 1):
            try:
                if method == 'get':
                    resp = self._session.get(url, headers=self._headers)
                elif method == 'post':
                    if form_data != None:
                        resp = self._session.post(url, data=form_data, headers=self._headers)
                elif method == 'put':
                    if form_data != None:
                        resp = self._session.put(url, data=form_data, headers=self._headers)
                
                resp.raise_for_status()
                result = True
                break
            except Exception as e:
                result = False
                log_msg = f"The http {method} method request for {url} failed with {str(num)} attempts."
                self._log.error(log_msg)
                
                # 如果非网络问题或系统问题，则打印日志
                if isinstance(e, requests.HTTPError):
                    self._log.info(e)
                    self._log.info(resp.text)
                
                log_msg = f"Wait a moment and try again..."
                self._log.info(log_msg)
                utils.pause(1, 2)

        log_msg = f"After {str(num)} attempts, the http {method} method request for {url} was {str(result)}."
        self._log.info(log_msg)
        return result, resp
    

    # 随机获取headers,静态方法
    @staticmethod
    def getheaders():
        headers_list = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Connection": "close",
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Connection": "close",
            },
        ]
        return random.choice(headers_list)
