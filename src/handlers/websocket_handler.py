import logging
from typing import *
from fastapi import WebSocket

import aiohttp
from ujson import dumps

from ..blivedm import (
    BaseHandler, BLiveClient, HeartbeatMessage, DanmakuMessage,
    GiftMessage, GuardBuyMessage, SuperChatMessage, SuperChatDeleteMessage
)

logger: logging.Logger = logging.getLogger('MocaBliveAPI')


async def _send_live_info_via_websocket(room_id: int, ws: WebSocket, message: Dict[str, Any]) -> None:
    """
    将接收到的直播数据通过websocket转发
    """
    body: Dict[str, Any] = dict(message, room_id=room_id)
    await ws.send_json(body)


class WebSocketHandler(BaseHandler):
    async def _on_heartbeat(self, client: BLiveClient, message: HeartbeatMessage, opts: Optional[Dict[str, Any]]):
        """
        收到心跳包（人气值）
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage, opts: Optional[Dict[str, Any]]):
        """
        收到弹幕
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))

    async def _on_gift(self, client: BLiveClient, message: GiftMessage, opts: Optional[Dict[str, Any]]):
        """
        收到礼物
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))

    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage, opts: Optional[Dict[str, Any]]):
        """
        有人上舰
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage, opts: Optional[Dict[str, Any]]):
        """
        醒目留言
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))

    async def _on_super_chat_delete(self, client: BLiveClient, message: SuperChatDeleteMessage,
                                    opts: Optional[Dict[str, Any]]):
        """
        删除醒目留言
        """
        await _send_live_info_via_websocket(client.room_id, opts['WS'], vars(message))
