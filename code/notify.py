'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC else001@sina.com
LastEditors: WT-W-PC else001@sina.com
LastEditTime: 2023-12-01 16:49:20
Description: 
支持bark app消息推送
'''

import urllib.parse
from robustreq import ReqRobot
import utils

BARK_BASE_URL = 'https://api.day.app'

# 支持bark推送消息
class Message(ReqRobot):
    def __init__(self, bark_key, retries=20):
        super().__init__(retries)
        self._bark_key = bark_key
        self._bark_url = f'{BARK_BASE_URL}/{str(self._bark_key)}/'
        
    # 推送bark消息
    def push(self, msg):
        push_message = f'{utils.getlocaltime()} {str(msg)}'
        dest_push_message = urllib.parse.quote_plus(push_message)

        notify_url = self._bark_url + dest_push_message
        
        result, resp = self.reqget(notify_url)
        
        log_msg = f'Bark: Pushing message {str(msg)} to user {self._bark_key} was {str(result)}'
        self._log.info(log_msg)
        return result