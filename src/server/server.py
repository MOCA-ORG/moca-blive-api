# Ω*
#               ■          ■■■■■  
#               ■         ■■   ■■ 
#               ■        ■■     ■ 
#               ■        ■■       
#     ■■■■■     ■        ■■■      
#    ■■   ■■    ■         ■■■     
#   ■■     ■■   ■          ■■■■   
#   ■■     ■■   ■            ■■■■ 
#   ■■■■■■■■■   ■              ■■■
#   ■■          ■               ■■
#   ■■          ■               ■■
#   ■■     ■    ■        ■■     ■■
#    ■■   ■■    ■   ■■■  ■■■   ■■ 
#     ■■■■■     ■   ■■■    ■■■■■


"""
Copyright (c) 2020.5.28 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaSystem/LICENSE/
"""

# -- Imports --------------------------------------------------------------------------

from .MocaBliveAPIServer import MocaBliveAPIServer
from ssl import SSLContext
from src.core import moca_config, LOG_DIR, VERSION, TOP_DIR
from src.moca_modules.moca_utils import *
from subprocess import call
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from sanic.websocket import WebSocketConnection
from sanic.exceptions import InvalidUsage
from src.moca_modules.moca_access import MocaAccess
from src.moca_modules.moca_mysql import MocaMysql
from src.moca_modules.moca_redis import MocaRedis
from src.blive_api import RawBLiveClient, InitError
from ujson import loads
from sys import executable
from asyncio import sleep
from src.database import get_comments, get_gifts

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

access: MocaAccess = MocaAccess(
    MocaRedis(
        moca_config.get('redis_host', '127.0.0.1'),
        moca_config.get('redis_port', 6379),
        moca_config.get('redis_pass', 'pass'),
        moca_config.get('redis_db_index', 0),
    ),
    MocaMysql(
        moca_config.get('mysql_host', '127.0.0.1'),
        moca_config.get('mysql_port', 3306),
        moca_config.get('mysql_user', 'root'),
        moca_config.get('mysql_pass', 'pass'),
        moca_config.get('mysql_db', 'moca_blive_api'),
    ),
    '64 per seconds'
)

allowed_origin: str = moca_config.get('origin')

blive_api: Blueprint = Blueprint('blive_api', 'blive')

# -------------------------------------------------------------------------- Variables --

# -- Server --------------------------------------------------------------------------

ssl: Optional[SSLContext]
if isinstance(moca_config.get('certfile'), str) and \
        isinstance(moca_config.get('keyfile'), str) and \
        Path(moca_config.get('certfile')).is_file() and \
        Path(moca_config.get('keyfile')).is_file():
    ssl = MocaBliveAPIServer.create_ssl_context(moca_config.get('certfile'),
                                                moca_config.get('keyfile'))
else:
    ssl = None

server: MocaBliveAPIServer = MocaBliveAPIServer(
    'MocaBliveAPIServer',
    moca_config.get('host'),
    moca_config.get('port'),
    ssl,
    LOG_DIR,
    None,
    moca_config.get('access_log'),
    moca_config.get('use_ipv6'),
    0,
    moca_config.get('headers')
)

server.add_blueprint(blive_api)

app = server.app

# -------------------------------------------------------------------------- Server --

# -- Blueprint --------------------------------------------------------------------------


@blive_api.route('/version')
async def version(request: Request) -> HTTPResponse:
    return text(VERSION)


@blive_api.route('/listen')
async def listen(request: Request) -> HTTPResponse:
    res = await app.redis.execute('KEYS', 'mr-moca-blive-api-pid-*')
    return json([item.decode()[22:] for item in res])


@blive_api.route('/select-comments')
async def select_comments(request: Request) -> HTTPResponse:
    try:
        json_data = request.json if isinstance(request.json, dict) else {}
    except InvalidUsage:
        json_data = {}
    room_id = json_data.get(
        'room_id', request.args.get('room_id', request.form.get('room_id', request.headers.get('ROOM-ID')))
    )
    start = json_data.get(
        'start', request.args.get('start', request.form.get('start', request.headers.get('Start')))
    )
    limit = json_data.get(
        'limit', request.args.get('limit', request.form.get('limit', request.headers.get('Limit')))
    )
    try:
        start = int(start)
    except (ValueError, TypeError):
        pass
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        pass
    if room_id is None:
        return text('ROOM_ID_IS_REQUIRED')
    elif not isinstance(room_id, str):
        return text('ROOM_ID_FORMAT_ERROR')
    elif len(room_id) > 32:
        return text('ROOM_ID_LENGTH_ERROR')
    if start is None:
        start = 0
    elif (not isinstance(start, int)) or (start < 0):
        return text('START_INDEX_FORMAT_ERROR')
    if limit is None:
        limit = 1024
    elif (not isinstance(limit, int)) or (limit < 0):
        return text('LIMIT_FORMAT_ERROR')

    pool = await app.mysql.get_aio_pool()
    data = await get_comments(pool, room_id, start, limit)
    return json(data)


@blive_api.route('/select-gifts')
async def select_gifts(request: Request) -> HTTPResponse:
    try:
        json_data = request.json if isinstance(request.json, dict) else {}
    except InvalidUsage:
        json_data = {}
    room_id = json_data.get(
        'room_id', request.args.get('room_id', request.form.get('room_id', request.headers.get('ROOM-ID')))
    )
    start = json_data.get(
        'start', request.args.get('start', request.form.get('start', request.headers.get('Start')))
    )
    limit = json_data.get(
        'limit', request.args.get('limit', request.form.get('limit', request.headers.get('Limit')))
    )
    try:
        start = int(start)
    except (ValueError, TypeError):
        pass
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        pass
    if room_id is None:
        return text('ROOM_ID_IS_REQUIRED')
    elif not isinstance(room_id, str):
        return text('ROOM_ID_FORMAT_ERROR')
    elif len(room_id) > 32:
        return text('ROOM_ID_LENGTH_ERROR')
    if start is None:
        start = 0
    elif (not isinstance(start, int)) or (start < 0):
        return text('START_INDEX_FORMAT_ERROR')
    if limit is None:
        limit = 1024
    elif (not isinstance(limit, int)) or (limit < 0):
        return text('LIMIT_FORMAT_ERROR')

    pool = await app.mysql.get_aio_pool()
    data = await get_gifts(pool, room_id, start, limit)
    return json(data)


@blive_api.websocket('/raw')
async def raw(request: Request, ws: WebSocketConnection):
    info = loads(await ws.recv())
    origin: str = request.headers.get('origin', 'None')
    if (info.get('room_id') is None) or (info.get('secret_key') is None):
        await app.moca_log.save(
            f'IP: 连接失败。类型: RawBLiveClient, 状态: 数据格式错误, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    elif (allowed_origin != '*') and not origin.startswith(allowed_origin):
        await app.moca_log.save(
            f'IP: 连接失败。类型: RawBLiveClient, 状态: origin认证失败, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    elif info.get('secret_key', '') != app.moca_config.get('secret_key', ''):
        await app.moca_log.save(
            f'IP: 连接失败。类型: RawBLiveClient, 状态: secret_key认证失败, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    else:
        await app.moca_log.save(
            f'IP: 开始连接。类型: RawBLiveClient, 状态: 成功, 房间号: {info.get("room_id")}', 1
        )
        client = RawBLiveClient(info['room_id'], ws, app, app.moca_config)
        try:
            await client.start()
        except InitError:
            await ws.send('ROOM_ID_ERROR')
        finally:
            await client.close()
        await app.moca_log.save(
            f'IP: 停止连接。类型: RawBLiveClient, 状态: 成功, 房间号: {info.get("room_id")}', 1
        )


@blive_api.websocket('/live')
async def live(request: Request, ws: WebSocketConnection):
    info = loads(await ws.recv())
    origin: str = request.headers.get('origin', 'None')
    if (info.get('room_id') is None) or (info.get('secret_key') is None):
        await app.moca_log.save(
            f'IP: 连接失败。类型: DefaultBLiveClient, 状态: 数据格式错误, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    elif (allowed_origin != '*') and not origin.startswith(allowed_origin):
        await app.moca_log.save(
            f'IP: 连接失败。类型: DefaultBLiveClient, 状态: origin认证失败, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    elif info.get('secret_key', '') != app.moca_config.get('secret_key', ''):
        await app.moca_log.save(
            f'IP: 连接失败。类型: DefaultBLiveClient, 状态: secret_key认证失败, 房间号: {info.get("room_id")}', 1
        )
        await ws.send('DENIED')
    else:
        await app.moca_log.save(
            f'IP: 开始连接。类型: DefaultBLiveClient, 状态: 成功, 房间号: {info.get("room_id")}', 1
        )
        count = await app.redis.increment('moca-blive-api-client-count' + info['room_id'])
        if count == 1:
            call(
                f'nohup {executable} "{str(TOP_DIR.joinpath("moca.py"))}"'
                f' run-listener {info["room_id"]} &> /dev/null &',
                shell=True
            )
        try:
            index = await app.redis.llen('moca-blive-api-' + info['room_id'])
            while True:
                data = await app.redis.lrange('moca-blive-api-' + info['room_id'], index, -1)
                index += len(data)
                await sleep(0.1)
                for item in data:
                    await ws.send(dumps(item))
        finally:
            await app.moca_log.save(
                f'IP: 停止连接。类型: DefaultBLiveClient, 状态: 成功, 房间号: {info.get("room_id")}', 1
            )
            count = await app.redis.decrement('moca-blive-api-client-count' + info['room_id'])
            if count == 0:
                pid = await app.redis.get('moca-blive-api-pid-' + info['room_id'])
                call(f'kill {pid}', shell=True)
                await app.redis.delete('moca-blive-api-pid-' + info['room_id'])

# -------------------------------------------------------------------------- Blueprint --
