'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC else001@sina.com
LastEditors: WT-H-PC else001@sina.com
LastEditTime: 2023-12-02 10:45:21
Description: 
初始化环境
阿里云盘认证,根据阿里云盘返回的token,更新青龙面板环境变量aliyunpantoken的值
阿里云盘签到并领取当日奖励
把今日签到结果推送到bark app
'''

from qinglongapi import QinglongRobot
from notify import Message
from aliyunpanrobot import AliyunpanRobot
import utils

ALIYUNPAN_TOKEN_NAME = 'aliyunpantoken'
BARK_KEY_NAME = 'barkkey'

def wait():
  log_msg = f'休息一会...'
  utils.logging.info(log_msg)
  utils.pause()

if __name__ == "__main__":
  # 构建青龙API实例
  log_msg = f'开始构建青龙API实例...'
  utils.logging.info(log_msg)
  result = False
  notification = False
  ql = QinglongRobot()
  
  # 获取青龙面板的环境变量
  log_msg = f'开始获取青龙面板的环境变量...'
  utils.logging.info(log_msg)
  if ql.initenv():
    wait()
    
    bark_key_id, bark_key_value = ql.getenv(BARK_KEY_NAME)
    aliyunpan_token_id, aliyunpan_token_value = ql.getenv(ALIYUNPAN_TOKEN_NAME)
    
    # 构建阿里云盘签到实例
    log_msg = f'开始构建阿里云盘签到实例...'
    utils.logging.info(log_msg)
    if aliyunpan_token_value != '':
      aliyunpan = AliyunpanRobot(aliyunpan_token_value)
      result = True
    else:
      result = False
      log_msg = f'青龙面板环境变量缺少 {BARK_KEY_NAME} 项.'
      utils.logging.error(log_msg)
      
    # 构建推送实例
    log_msg = f'开始构建推送实例...'
    utils.logging.info(log_msg)
    if bark_key_value != '':
      bark = Message(bark_key_value)
      notification = True
    else:
      log_msg = f'青龙面板环境变量缺少 {BARK_KEY_NAME} 的值.'
      utils.logging.info(log_msg)
    
    if result:
      # 阿里云盘认证
      log_msg = f'开始阿里云盘认证...'
      utils.logging.info(log_msg)
      if aliyunpan.auth():
        wait()
        
        # 根据返回的refreshtoken,更新青龙面板环境变量aliyunpantoken的值
        log_msg = f'开始根据阿里云盘返回的token,更新青龙面板环境变量aliyunpantoken的值...'
        utils.logging.info(log_msg)
        if ql.updateenv(ALIYUNPAN_TOKEN_NAME, aliyunpan.refresh_token):
          wait()
          
          # 阿里云盘签到
          log_msg = f'开始阿里云盘签到...'
          utils.logging.info(log_msg)
          if aliyunpan.signin():
            wait()
            
            # 领取今日奖励
            log_msg = f'开始领取今日奖励...'
            utils.logging.info(log_msg)
            if aliyunpan.receiveaward():
              wait()
              
              log_msg = f'阿里云盘：今日签到成功，{aliyunpan.today_reward}\n本月累计签到 {aliyunpan.sign_in_count} 天'
            else:
              result = False
          else:
            result = False
        else:
          result = False
    else:
      result = False  
  else:
    result = False
    
  if not result:
    log_msg = f'阿里云盘今日签到失败！请手工补签！'
    
  utils.logging.info(log_msg)
  if notification:
    bark.push(log_msg)
    
pass