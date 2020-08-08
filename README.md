## 通过websocket和JSON向前端app提供关于哔哩哔哩直播的各种API

#### 哔哩哔哩直播的监听部分来自这个项目 https://github.com/xfgryujk/blivedm

#### 请使用Python3.7以上
#### 仅在Mac和Linux系统进行过检测，Windows系统没测试过

## 安装方法
```bash
git clone https://github.com/el-ideal-ideas/MocaBliveAPI.git
cd ./MocaBliveAPI
python3 -m pip install -r requirements.txt
```

## 运行方法
```bash
python3 moca.py run
```

## 在后台运行（Linux系统）
```bash
nohup python3 moca.py run &> /dev/null &
```

## 使用方法
- 用websocket连接服务器。`ws://<服务器的IP>:服务器的端口/blive/live` 比如 `ws://127.0.0.1:5992/blive/live`
- 如果想获取未处理的全部数据，可以连接`ws://<服务器的IP>:服务器的端口/blive/raw`
- 发送认证信息(JSON格式)
```json
{
   "room_id": "想监听的直播间的房间号",
   "secret_key": "自定义的API秘钥。需要和config.json文件里面一致"
}
```
- 之后服务器会实时向客服端发送直播信息。

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

## 什么是房间号
- 如果直播间的URL是`https://live.bilibili.com/123456`
- 那么房间号就是`123456`
- 房间号是每个账号固定的，不会改变。

## 设定
#### 全部设定都在 config.json 文件内

```
{
 "access_log": true, 是否保存访问记录
 "blive_comment_api_gift_id_list": [  已知的礼物ID （发现未知ID的时候会在日志里面记录）
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
  "30508",
  "30607"
 ],
 "certfile": "",  如果需要SSL请填写认证文件地址
 "headers": {  头文件信息

 },
 "host": "0.0.0.0",  API服务器的IP。
 "keyfile": "",  如果需要SSL请填写认证文件地址
 "log_rotate": false,  是否根据日期把日志分成多个文件。
 "mysql_db": "moca_blive_api",  mysql数据库名
 "mysql_host": "127.0.0.1",   mysql数据库IP
 "mysql_pass": "mochimochi",    mysql数据库密码
 "mysql_port": 3306,  mysql数据库端口
 "mysql_user": "root",  mysql数据库用户名
 "origin": "*",  根据http请求的头文件可以限制请求来源。*代表不限制任何来源
 "port": 5992,  API服务器端口
 "redis_db_index": 0, redis数据库的索引
 "redis_host": "127.0.0.1",  redis数据库的IP
 "redis_pass": "",  redis数据库的密码
 "redis_port": 6379,  redis数据库的端口
 "secret_key": "mochimochi",  API秘钥
 "use_ipv6": false  是否使用IPv6
}
```


## HTTP功能
- `/blive/version`
    - 返回API服务器版本信息
- `/blive/listen`
    - 返回监听中的房间名
- `/blive/select-comments`
    - 返回已经保存在数据库内的留言内容
    - http请求参数
        - room_id: 房间号
        - start: 从第几个留言开始获取，0代表最开始
        - limit: 最大获取数量。
- `/blive/select-gifts`
    - 返回已经保存在数据库内的礼物记录
    - http请求参数
        - room_id: 房间号
        - start: 从第几个礼物记录开始获取，0代表最开始
        - limit: 最大获取数量。
    
## License (MIT)
MIT License

Copyright 2020.5.28 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.