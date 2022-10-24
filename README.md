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
