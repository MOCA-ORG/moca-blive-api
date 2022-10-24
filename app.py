from typing import *
from src.handlers import DebugHandler, POSTHandler
from src.blivedm import BLiveClient
from src.libs import get_live_info, get_live_status, get_user_info, get_user_icon, get_user_name
from typer import Typer
from pprint import pp
import asyncio
import logging
import sys
from os import environ
import uvicorn
from src.server import app


console: Typer = Typer()
logger: logging.Logger = logging.getLogger('MocaBliveAPI')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@console.command('server')
def server_cmd(port: int = 3000):
    """
    启动websocket服务器
    """
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=port
    )


@console.command('debug')
def debug_cmd(room_ids: List[int]):
    """
    用于查看各种直播数据
    """

    async def _run():
        handler: DebugHandler = DebugHandler()
        clients: List[BLiveClient] = [BLiveClient(room_id) for room_id in room_ids]

        for client in clients:
            client.add_handler(handler)
            client.start()

        try:
            await asyncio.gather(*(
                client.join() for client in clients
            ))
        finally:
            await asyncio.gather(*(
                client.stop_and_close() for client in clients
            ))

    logger.setLevel(logging.DEBUG)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('post')
def post_cmd(room_ids: List[int], url: Optional[str] = None):
    """
    将接收到的直播数据转发到指定URL
    """
    try:
        target = url or environ['POST_TO']
    except KeyError:
        logger.warning('请设置 "POST_TO" 环境变量，或者使用 --url 指定数据接收地址')
        return None

    async def _run():
        handler: POSTHandler = POSTHandler()
        clients: List[BLiveClient] = [BLiveClient(room_id, opts={'URL': target}) for room_id in room_ids]

        for client in clients:
            client.add_handler(handler)
            client.start()

        try:
            await asyncio.gather(*(
                client.join() for client in clients
            ))
        finally:
            await asyncio.gather(*(
                client.stop_and_close() for client in clients
            ))

    logger.setLevel(logging.DEBUG)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('live-info')
def live_info_cmd(room_id: str):
    """
    获取直播信息
    """

    async def _run():
        pp(await get_live_info(room_id))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('live-status')
def live_status_cmd(room_id: str):
    """
    获取直播信息
    """

    async def _run():
        print("直播状态: %s" % {0: '未开播', 1: '直播中', 2: '轮播中'}[await get_live_status(room_id)])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('user-info')
def user_info_cmd(user_id: str):
    """
    获取用户信息
    """

    async def _run():
        pp(await get_user_info(user_id))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('user-icon')
def user_icon_cmd(user_id: str):
    """
    获取用户头像
    """

    async def _run():
        print(await get_user_icon(user_id))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


@console.command('user-name')
def user_icon_cmd(user_id: str):
    """
    获取用户昵称
    """

    async def _run():
        print(await get_user_name(user_id))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())


console()
