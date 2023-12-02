<!--
 * @Author: WT-H-PC
 * @Date: 2023-12-01 22:42:12
 * @LastEditors: WT-H-PC
 * @LastEditTime: 2023-12-02 13:03:47
 * @Description: 
-->
<h1 align="center">阿里云盘签到</h1>

## 功能
支持在青龙面板（一个任务管理平台）环境下：
- 阿里云盘每日自动签到
- 领取当日奖励
- 实时推送签到结果到手机端的Bark应用
- 过滤网络干扰，运行稳定


## 运行环境
1. 【必要】安装青龙面板，安装参考链接：[青龙面板](https://github.com/whyour/qinglong)。
2. 【可选】手机安装Bark应用后，才能获取结果通知。


## 使用说明
gitee版本请参考 [https://gitee.com/hahaha2100/aliyunpansignin](https://gitee.com/hahaha2100/aliyunpansignin)
1. 订阅代码仓库。在青龙面板`订阅管理`界面，点击右上角的`创建订阅`按钮，录入完成后，点击`确定`按钮。输入项说明如下：
    - 名称：自定义填写，如填入`阿里云盘自动签到`
    - 类型：选择公开仓库
    - 链接：填入 https://github.com/hahaha2100/aliyunpansignin.git
    - 分支：main
    - 唯一值：系统自动生成，不用填写
    - 定时任务：选择crontab
    - 定时规则：自定义填写，如填入`30 8 * * *`（代表每天上午8点30分自动执行）
    - 自动添加任务：关闭
    - 自动删除任务：关闭
    - 其他未列出的输入项：不用填写<br/>

    录入完成后，会生成一条记录，拉到记录的最后面，点击`运行`按钮并查看青龙面板`脚本管理`界面，如果新生成了一个`hahaha2100_aliyunpansignin_main`文件夹，就说明成功了。

2. 设置环境变量。在青龙面板`环境变量`界面，点击右上角的`创建订阅`按钮，依次创建`aliyunpantoken`和`barkkey`两个环境变量。<br/>
    1. 创建aliyunpantoken环境变量
        - 名称：aliyunpantoken
        - 自动拆分：选择否
        - 值：获取方法如下,<br/>
            一、`Edge浏览器`登录`阿里云盘`，官网登录地址：[https://www.aliyundrive.com/drive](https://www.aliyundrive.com/drive)<br/>
            二、登录后，按下`F12`，根据下图找到`refresh_token`的值，复制填入即可。
            ![参考图片](https://pic.imgdb.cn/item/656a1b59c458853aefb0c0de.png)

    2. 创建barkkey环境变量(可选，影响消息推送)
        - 名称：barkkey
        - 自动拆分：选择否
        - 值：获取方法如下,<br/>
              一、手机下载应用Bark<br/>
              二、打开Bark应用，参考下图，找到`推送内容`下的链接，复制域名后面的一串字符`Xy4ssdd2pARjLfFY`填入即可。
            ```bash
            # 推送内容样式参考
            https://bark.gugu.ovh/Xy4ssdd2pARjLfFY/这里改成你自己的推送内容
            ```
            ![参考图片](https://pic.imgdb.cn/item/656a1b62c458853aefb0dc27.png)<br/>

    3. 查看是否有`CLIENT_ID`和`CLIENT_SECRET`这两个环境变量，如果有就可以跳过这一步。
        - 进入青龙面板`系统设置`界面，选择`应用设置`，点击右上角`创建应用`按钮。创建应用输入项如下：
            - 名称：随意填写
            - 权限：选择`环境变量`<br/>
            
            创建完成后，就可以在青龙面板`环境变量`界面，看到`CLIENT_ID`和`CLIENT_SECRET`这两个环境变量

3. 设置定时任务。在青龙面板`定时任务`界面，点击右上角的`创建任务`按钮，录入完成后，点击`确定`按钮。输入项说明如下:
    - 名称：自定义填写，如填入`阿里云盘自动签到`
    - 命令/脚本：填入`hahaha2100_aliyunpansignin_main/aliyunpansignin.py`
    - 定时规则：自定义填写，如填入`0 9 * * *`（代表每天上午9点整自动执行）
    - 其他未列出的输入项：不用填写

    录入完成后，会生成一条记录，点击`运行`按钮即可。

<h1 align="center">大功告成(^▽^)</h1>
