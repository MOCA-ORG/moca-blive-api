## 监听哔哩哔哩直播的API服务器
#### 哔哩哔哩直播的监听部分来自这个项目 https://github.com/xfgryujk/blivedm

#### 请使用Python3.7 

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
- 用websocket连接服务器。`ws://<服务器的IP>:服务器的端口/live` 比如 `ws://127.0.0.1:7899/live`
- 发送认证信息(JSON格式)
```json
{
   "cmd": "start",
   "room_id": "想监听的直播间的房间号",
   "api_key": "自定义的API秘钥。需要和config.json文件里面一致"
}
```
- 之后服务器会实时向客服端发送直播信息。

## 设定
#### 全部设定都在 config.json 文件内
```json
{
    "api_key": "API秘钥",
    "api_server_access_log": false, // 布尔值, 是否保存访问记录
    "api_server_certfile": "", // 如果使用SSL请配置认证文件地址
    "api_server_debug": false,  // 布尔值， 是否开启debug模式
    "api_server_host": "0.0.0.0", // 服务器IP地址
    "api_server_keyfile": "",  // 如果使用SSL请配置认证文件地址
    "api_server_port": 7899,  // 服务器端口
    "api_server_use_ipv6": false,  // 布尔值，是否使用IPv6
    "api_server_use_ssl": false,  // 布尔值，是否使用SSL
    "gift_id_list": [  // 已知的礼物ID，用于检测B站出新礼物。
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
        "20002"
    ],
    "mysql_dbname": "blive_comment_api", // 数据库名
    "mysql_host": "127.0.0.1",  // 数据库IP
    "mysql_pass": "", // 数据库密码
    "mysql_port": 3306, // 数据库端口
    "mysql_user": "root", // 数据库用户
    "save_comments": false, // 布尔值，是否保存留言到数据库。
    "save_gifts": false, // 布尔值，是否保存礼物记录到数据库。
    "send_mail_if_found_unknown_gift_name": false, // 布尔值， 如果发现新礼物，是否邮件通知。
    "smtp_from_address": "", // 发件人信息
    "smtp_mail_title": "BliveCommentAPI",  // 邮件名
    "smtp_server_host": "", // 邮件服务器IP
    "smtp_server_pass": "", // 邮件服务器密码
    "smtp_server_port": 25, // 邮件服务器端口
    "smtp_server_user": "", // 邮件服务器用户名
    "smtp_to_address": [], // 邮件接收邮箱清单
    "smtp_use_ssl": true // 发送邮件是否使用SSL
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
  "price": "金额",
}
```

## HTTP功能
- `/status`
    - 如果系统在运行，返回`BliveCommentAPI is running.`
- `/online`
    - 返回正在监听的直播间的清单。
    
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
