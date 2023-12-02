'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC
LastEditors: WT-W-PC
LastEditTime: 2023-12-01 19:04:20
Description: 
对青龙面板的API进行封装,获取青龙面板的环境变量
'''


import json
from robustreq import ReqRobot
from utils import assistant
import os

QL_BASE_URL = 'http://localhost:5700'


class QinglongRobot(ReqRobot):
    def __init__(self, retries=20):
        super().__init__(retries)
        self._client_id = os.environ.get('CLIENT_ID')
        self._client_secret = os.environ.get('CLIENT_SECRET')
        self._base_url = QL_BASE_URL
        self._login_url = f'{self._base_url}/open/auth/token?client_id={self._client_id}&client_secret={self._client_secret}'
        self._env_url =  f'{self._base_url}/open/envs'
        self.env_list = []
        # 是否初始化就绪
        self.__status = False

    def status(self):
        self.__status = False
        if self._client_id != '' and self._client_secret != '' and self.env_list != []:
            self.__status = True
        return self.__status

    # 登陆青龙面板
    @assistant('DEBUG')
    def _login(self):
        url = self._login_url
        result, resp = self.reqget(self._login_url)
        
        if result:
            try:
                re = resp.json()
                self.token = re['data']['token']
                headers = {
                    "Authorization": 'Bearer ' + self.token,
                    "User-Agent": "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4577.63 Safari/537.36",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Accept-Encoding": "gzip,deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "close"
                }
                self.setheaders(headers)
            except Exception as e:
                result = False
                log_msg = f"Parsing the results returned by {url} failed."
                self._log.exception(log_msg)
                self._log.exception(e)
                                
        log_msg = f"Login {url} was {str(result)}."
        self._log.info(log_msg)
        return result
        
    # 获取全量青龙面板的环境变量
    @assistant('DEBUG')
    def _getenvlist(self):
        url = self._env_url
        result, resp = self.reqget(self._env_url)

        if result:
            try:
                re = resp.json()
                self.env_list = re['data']
            except Exception as e:
                result = False
                log_msg = f"Parsing the results returned by {url} failed."
                self._log.exception(log_msg)
                self._log.exception(e)

        log_msg = f"Obtaining {url} environment variable list was {str(result)}."
        self._log.info(log_msg)
        return result
    
    # 初始化数据，登录并获取青龙面板的环境变量
    def initenv(self):
        result = self._login()
        if result:
            result = self._getenvlist()

        log_msg = f"Initializing the environment variables was {str(result)}."
        self._log.info(log_msg)
        return result
        
    # 从缓存中根据name属性获取对应的id与value值
    def getenv(self, key):
        id = '' 
        value = ''
        for env in self.env_list:
            if str(env['name']) == str(key):
                value = str(env['value'])
                id = str(env['id'])
                break
        return id, value
    
    # 根据环境变量的name值，更新环境变量的value值，调用之前需要确保是最新值
    @assistant('DEBUG')
    def updateenv(self, name, new_value):
        original_id, original_value = self.getenv(name)
        data = {
            "value": new_value,
            "name": name,
            "remarks": "QinglongRobot",
            "id": int(original_id)
        }
        form_data = json.dumps(data)
        
        url = self._env_url
        result, resp = self.reqput(self._env_url, form_data=form_data)

        log_msg = f"Updating {url} environment variable {str(name)} from {str(original_value)} to {str(new_value)} was {str(result)}."
        self._log.info(log_msg)
        return result