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
Copyright (c) 2020.1.17 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaLog/LICENSE/
"""


# -- Imports --------------------------------------------------------------------------

from sanic import Blueprint
from ujson import loads
from sanic.request import Request
from sanic.response import text
from sanic.websocket import WebSocketConnection
from .... import core
from ...app import app
from .default_blive_client import DefaultBLiveClient
from .raw_blive_client import RawBLiveClient
from .send_mail import send_start_listen_mail, send_stop_listen_mail
from .blivedm import InitError

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

blive: Blueprint = Blueprint('BLiveCommentAPI', 'blive')

# -------------------------------------------------------------------------- Variables --

# -- Routes --------------------------------------------------------------------------


@blive.route('/status', methods={'GET'})
async def status(request: Request):
    return text('BliveCommentAPI is running.')


@blive.websocket('/live')
async def live(request: Request, ws: WebSocketConnection):
    data = loads(await ws.recv())
    if data['cmd'] == 'start' and data['secret_key'] == core.config.get('blive_comment_api_secret_key', str, ''):
        client = DefaultBLiveClient(room_id=data['room_id'], loop=app.loop, ws=ws, app=app)
        try:
            await app.logger.save(f"开始监听直播: {data['room_id']}", app.logger.INFO)
            await send_start_listen_mail(f"开始监听直播: {data['room_id']}", app.logger)
            await client.start()
        except InitError:
            await ws.send('ROOM ID ERROR')
        finally:
            await app.logger.save(f"停止监听直播: {data['room_id']}", app.logger.INFO)
            await send_stop_listen_mail(f"停止监听直播: {data['room_id']}", app.logger)
            await client.close()
    else:
        await ws.send('SECRET KEY ERROR')


@blive.websocket('/raw')
async def raw(request: Request, ws: WebSocketConnection):
    data = loads(await ws.recv())
    if data['cmd'] == 'start' and data['secret_key'] == core.config.get('blive_comment_api_secret_key', str, ''):
        client = RawBLiveClient(room_id=data['room_id'], loop=app.loop, ws=ws, app=app)
        try:
            await app.logger.save(f"开始监听直播: {data['room_id']}", app.logger.INFO)
            await send_start_listen_mail(f"开始监听直播: {data['room_id']}", app.logger)
            await client.start()
        except InitError:
            await ws.send('ROOM ID ERROR')
        finally:
            await app.logger.save(f"停止监听直播: {data['room_id']}", app.logger.INFO)
            await send_stop_listen_mail(f"停止监听直播: {data['room_id']}", app.logger)
            await client.close()
    else:
        await ws.send('SECRET KEY ERROR')

# -------------------------------------------------------------------------- Routes --
