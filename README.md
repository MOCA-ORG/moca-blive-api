## 通过websocket和JSON向前端app提供关于哔哩哔哩直播的各种API

#### 哔哩哔哩直播的监听部分来自这个项目 https://github.com/xfgryujk/blivedm

#### 请使用Python3.10以上

## 安装方法
```bash
git clone https://github.com/MOCABEROS-TEAM/MocaBliveAPI.git
cd ./MocaBliveAPI
python3 -m pip install -r requirements.txt
```

## 运行方法
```bash
# 启动api服务器
python3 app.py server --port 8080

# 显示其他功能
python app.py --help
```

## 使用方法
- 用websocket连接服务器。`ws://<服务器的IP>:服务器的端口/live` 比如 `ws://127.0.0.1:8080/live`
- 发送认证信息(JSON格式)
```json
{
   "room_id": "想监听的直播间的房间号",
   "secret_key": "自定义的API秘钥。通过环境变量 `SECRET_KEY` 设置"
}
```
- 之后服务器会实时向客户端发送直播信息。

## License (MIT)
MIT License

Copyright 2022.10.24 <mocaberos>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.