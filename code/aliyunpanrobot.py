'''
Date: 2023-12-01 12:19:01
Author: WT-W-PC else001@sina.com
LastEditors: WT-H-PC else001@sina.com
LastEditTime: 2023-12-02 10:44:51
Description: 
支持阿里云盘签到并领取今日奖励
'''

from robustreq import ReqRobot
import json

ALIYUN_BASE_URL = 'https://member.aliyundrive.com/v1/activity'
ALIYUN_AUTH_URL = 'https://auth.aliyundrive.com/v2/account/token'
ALIYUN_SIGN_IN_URL = 'https://member.aliyundrive.com/v1/activity/sign_in_list?_rx-s=mobile'
ALIYUN_REWARD_URL = 'https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile'

HEADERS = {
"User-Agent": "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4577.63 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8",
"Accept-Encoding": "gzip,deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "close"
}


class AliyunpanRobot(ReqRobot):
  def __init__(self, token, retries=20):
    super().__init__(retries)
    # 原始token
    self.token = token
    # 登陆后更新后的token
    self.refresh_token = ''
    # 签到使用的token
    self.access_token = ''
    
    self.base_url = ALIYUN_BASE_URL
    self.auth_url = ALIYUN_AUTH_URL
    self.sign_in_url = ALIYUN_SIGN_IN_URL
    self.reward_url = ALIYUN_REWARD_URL
    
    self.setheaders(HEADERS)

      
  # 进行阿里云认证
  def auth(self):
    data = {
      "grant_type": "refresh_token",
      "refresh_token": self.token
    }
    form_data = json.dumps(data)
    
    url = self.auth_url
    result, resp = self.reqpost(self.auth_url, form_data=form_data)
    if result:
        try:
          re = resp.json()
          self.refresh_token = str(re['refresh_token'])
          self.access_token = str(re['access_token'])
        except Exception as e:
          result = False
          log_msg = f"Parsing the results returned by {url} failed."
          self._log.exception(log_msg)
          self._log.exception(e)
          
    log_msg = f"Authentication in {url} was {str(result)}"
    self._log.info(log_msg)
    return result
  
  # 阿里云签到
  def signin(self):
    self._headers['Authorization'] = self.access_token
    self._headers['Content-Type'] = 'application/json'
    data = {
      "isReward": False
    }
    form_data = json.dumps(data)
    url = self.sign_in_url
    result, resp = self.reqpost(self.sign_in_url, form_data=form_data)
    
    if result:
      try:
        re = resp.json()
        # 长字典，记录了所有历史签到记录
        self.sign_in_logs = re['result']['signInLogs']
        # 当月累计签到天数
        self.sign_in_count = re['result']['signInCount']
        # 最后一条记录即为当天的签到记录
        self.current_sign_in_info = self.sign_in_logs[int(self.sign_in_count) - 1]
        log_msg = f"The total number of sign-in days the month is {str(self.sign_in_count)} days"
        self._log.info(log_msg)
        result = True
      except Exception as e:
        result = False
        log_msg = f"Parsing the results returned by {url} failed."
        self._log.exception(log_msg)
        self._log.exception(e)
        
    log_msg = f"Sign-in on {url} was {str(result)}"
    self._log.info(log_msg)
    return result
  
  # 领取今日签到奖励
  def receiveaward(self):
    result = False
    # 如果没有领取今日奖励则进行领取
    if not self.current_sign_in_info['isReward']:
      data = {
        "signInDay": self.current_sign_in_info['day']
        }
      form_data = json.dumps(data)
      
      # 领取奖励
      url = self.reward_url
      result, resp = self.reqpost(self.reward_url, form_data=form_data)
      if result:
        try:
          re = resp.json()
          self.today_reward = f"{str(re['result']['notice'])}, {str(re['result']['subNotice'])}"
          log_msg = f"On day {str(self.current_sign_in_info['day'])}, the reward was successfully claimed, and got {self.today_reward}"
          self._log.info(log_msg)
        except Exception as e:
          result = False
          log_msg = f"Parsing the results returned by {url} failed."
          self._log.exception(log_msg)
          self._log.exception(e)
    # 今日领取过奖励则直接返回
    else:
      result = True
      self.today_reward = f"{str(self.current_sign_in_info['reward']['notice'])}, {str(self.current_sign_in_info['reward']['subNotice'])}"
      log_msg = f"On day {str(self.current_sign_in_info['day'])}, the reward had been successfully claimed, and got {self.today_reward}"
      self._log.info(log_msg)
    return result