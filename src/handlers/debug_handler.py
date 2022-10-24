import logging
from typing import *

from ..blivedm import (
    BaseHandler, BLiveClient, HeartbeatMessage, DanmakuMessage, GiftMessage, GuardBuyMessage, SuperChatMessage,
    SuperChatDeleteMessage
)

logger: logging.Logger = logging.getLogger('MocaBliveAPI')


class DebugHandler(BaseHandler):
    async def _on_heartbeat(self, client: BLiveClient, message: HeartbeatMessage, opts: Optional[Dict[str, Any]]):
        """
        收到心跳包（人气值）
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 收到心跳包（人气值） ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))

    async def _on_danmaku(self, client: BLiveClient, message: DanmakuMessage, opts: Optional[Dict[str, Any]]):
        """
        收到弹幕
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 收到弹幕 ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))

    async def _on_gift(self, client: BLiveClient, message: GiftMessage, opts: Optional[Dict[str, Any]]):
        """
        收到礼物
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 收到礼物 ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))

    async def _on_buy_guard(self, client: BLiveClient, message: GuardBuyMessage, opts: Optional[Dict[str, Any]]):
        """
        有人上舰
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 有人上舰 ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))

    async def _on_super_chat(self, client: BLiveClient, message: SuperChatMessage, opts: Optional[Dict[str, Any]]):
        """
        醒目留言
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 醒目留言 ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))

    async def _on_super_chat_delete(self, client: BLiveClient, message: SuperChatDeleteMessage,
                                    opts: Optional[Dict[str, Any]]):
        """
        删除醒目留言
        """
        params: Dict[str, Any] = vars(message)
        logger.debug('\n---- 删除醒目留言 ----\n' + ''.join([f'{key}: \t{params[key]}\n' for key in params]))
