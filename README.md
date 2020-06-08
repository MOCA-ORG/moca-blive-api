## 通过websocket和JSON像前端app提供关于哔哩哔哩直播的各种API

#### 哔哩哔哩直播的监听部分来自这个项目 https://github.com/xfgryujk/blivedm

#### 请使用Python3.7 
#### 仅在Mac和Linux系统进行过检测，Windows系统没测试过

## 安装方法
```bash
git clone https://github.com/el-ideal-ideas/BliveCommentAPI.git
cd ./BliveCommentAPI
python3 -m pip install -r requirements.txt
```

## 运行方法
```bash
python3 blive_comment_api_server.py
```

## 在后台运行（Linux系统）
```bash
nohup python3 blive_comment_api_server.py > /dev/null &
```

## 使用方法
- 用websocket连接服务器。`ws://<服务器的IP>:服务器的端口/blive/live` 比如 `ws://127.0.0.1:7899/blive/live`
- 如果想获取未处理的全部数据，可以连接`ws://<服务器的IP>:服务器的端口/blive/raw`
- 发送认证信息(JSON格式)
```json
{
   "cmd": "start",
   "room_id": "想监听的直播间的房间号",
   "secret_key": "自定义的API秘钥。需要和config.json文件里面一致"
}
```
- 之后服务器会实时向客服端发送直播信息。

## 什么是房间号
- 如果直播间的URL是`https://live.bilibili.com/123456`
- 那么房间号就是`123456`
- 房间号是每个账号固定的，不会改变。

## 设定
#### 全部设定都在 config.json 文件内

```
{
    "api_server_access_log": true, // 是否记录访问记录
    "api_server_debug": false, // 是否开启Sanic服务器的debug模式
    "api_server_host": "0.0.0.0", // 服务器IP
    "api_server_port": 7899, // 服务器端口 
    "api_server_use_ipv6": false, // 是否用IPv6
    "api_server_worker_number": 8, // 可使用的进程数量
    "blive_comment_api_gift_id_list": [  // 已知礼物ID清单
        "1",
        "3",
        "25",
        "7",
        "8",
        "39",
        "20003",
        "20004",
        "20008",
        "20014",
        "30004",
        "30046",
        "30063",
        "30064",
        "30072",
        "30087",
        "30090",
        "30135",
        "30136",
        "30143",
        "30144",
        "30145",
        "30204",
        "550001",
        "550002",
        "550003",
        "550004",
        "550005",
        "30205",
        "20002",
        "30508"
    ],
    "blive_comment_api_save_comments": false,  // 是否保存留言到数据库
    "blive_comment_api_save_gifts": false, // 是否保存礼物记录到数据库
    "blive_comment_api_save_raw_data": false, // 是否保存json数据到数据库
    "blive_comment_api_secret_key": "请自定义一个字符串",  // API秘钥，请设定一个随机的字符串
    "blive_comment_api_send_mail_if_found_unknown_gift_name": false, // 如果发现未知礼物ID，发送邮件通知
    "blive_comment_api_send_mail_if_start_listen": false,  // 如果开始监控直播，发送邮件通知
    "blive_comment_api_send_mail_if_stop_listen": false,  // 如果停止监控直播， 发送邮件通知
    "certfile": "",  // 如果需要SSL请填写认证文件地址
    "keyfile": "",  // 如果需要SSL请填写认证文件地址
    "log_level": 1,  // 日志等级
    "mysql_dbname": "blive_comment_api",   // 数据库名
    "mysql_host": "127.0.0.1",   // 数据库IP
    "mysql_max_size": 10,   //连接池上限
    "mysql_min_size": 1,   // 连接池下限
    "mysql_pass": "",   // 数据库密码
    "mysql_port": 3306,   // 数据库端口
    "mysql_user": "root",   // 数据库用户名
    "send_notification_when_critical_error_occurred": false,   // 如果发生了无法解决的异常，尝试邮件通知
    "send_notification_when_error_occurred": false,   // 如果发生了异常， 尝试邮件通知
    "smtp_host": "",   // 邮件服务器IP
    "smtp_notification_from_address": "",   // 发件人邮箱
    "smtp_notification_pass": "",   // 邮件服务器密码
    "smtp_notification_to_address": [   // 接受人邮箱清单
        ""
    ],
    "smtp_notification_user": "",    // 邮件服务器用户名
    "smtp_port": 465,  // 邮件服务器 端口
    "smtp_use_ssl": true   // 是否用ssl访问邮件服务器
}
```

## 信息
- 弹幕
```json
{
   "cmd": "danmaku",
   "uname": "用户名",
   "msg": "弹幕内容"
}
```
- 礼物
```json
{
  "cmd": "gift",
  "uname": "用户名",
  "gift_name": "礼物名",
  "gift_id": "礼物ID",
  "gift_num": "礼物数量",
  "coin_type": "金瓜子还是银瓜子",
  "total_coin": "瓜子数量"
}
```
- 上舰队
```json
{
  "cmd": "buy_guard",
  "uname": "用户名",
  "guard_type": "1总督，2提督，3舰长"
}
```
- 醒目留言
```json
{
  "cmd": "super_chat",
  "uname": "用户名",
  "msg": "留言",
  "price": "金额"
}
```

## HTTP功能
- `/status`
    - 如果系统在运行，返回`BliveCommentAPI is running.`
    
## License (MIT)
MIT License

Copyright 2020.1.17 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
