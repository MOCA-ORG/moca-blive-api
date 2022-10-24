import logging
from typing import *

import aiohttp
from ujson import dumps

from ..blivedm import (
    BaseHandler, BLiveClient, HeartbeatMessage, DanmakuMessage,
    GiftMessage, GuardBuyMessage, SuperChatMessage, SuperChatDeleteMessage
)

logger: logging.Logger = logging.getLogger('MocaBliveAPI')


async def _post_message_to_target_server(room_id: int, url: str, message: Dict[str, Any]) -> None:
    """
    将接收到的直播数据转发到指定URL
    """
    body: Dict[str, Any] = dict(message, room_id=room_id)
    async with aiohttp.ClientSession(json_serialize=dumps) as session:
        async with session.post(url, json=body) as res:
            if res.status != 200:
                logger.error('POST "%s", status=%d, reason=%s, message=%s', url, res.status, res.reason, dumps(body))


class POSTHandler(BaseHandler):
    async def _on_heartbeat(self, client: BLiveClient, message: HeartbeatMessage, opts: Optional[Dict[str, Any]]):
        """
        收到心跳包（人气值）
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage, opts: Optional[Dict[str, Any]]):
        """
        收到弹幕
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))

    async def _on_gift(self, client: BLiveClient, message: GiftMessage, opts: Optional[Dict[str, Any]]):
        """
        收到礼物
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))

    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage, opts: Optional[Dict[str, Any]]):
        """
        有人上舰
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage, opts: Optional[Dict[str, Any]]):
        """
        醒目留言
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))

    async def _on_super_chat_delete(self, client: BLiveClient, message: SuperChatDeleteMessage,
                                    opts: Optional[Dict[str, Any]]):
        """
        删除醒目留言
        """
        await _post_message_to_target_server(client.room_id, opts['URL'], vars(message))
