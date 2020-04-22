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

from .send_mail import send_unknown_gift_mail
from . import blivedm
from aiohttp import ClientSession
from ujson import dumps
from ... import core

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

core.config.get('blive_comment_api_gift_id_list', list, ["1", "3", "25", "7", "8", "39", "20003", "20004", "20008",
                                                         "20014", "30004", "30046", "30063", "30064", "30072", "30087",
                                                         "30090", "30135", "30136", "30143", "30144", "30145", "30204",
                                                         "550001", "550002", "550003", "550004", "550005", "30205",
                                                         "20002", "30508"])

# -------------------------------------------------------------------------- Init --

insert_gift = """
insert into user_gifts(room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin) 
values(%s, %s, %s, %s, %s, %s, %s);
"""

insert_comment = """
insert into user_comments(room_id, user_name, comment) 
values(%s, %s, %s);
"""

# -- DefaultBLiveClient --------------------------------------------------------------------------


class DefaultBLiveClient(blivedm.BLiveClient):
    # 自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    def __init__(self, room_id, uid=0, session: ClientSession = None,
                 heartbeat_interval=30, ssl=True, loop=None, ws=None, app=None):
        super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)
        self._ws = ws
        self._app = app

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        if core.config.get('blive_comment_api_save_comments', bool, False):
            async with self._app.mysql_pool.acquire() as con:
                async with con.cursor() as cur:
                    await cur.execute(insert_comment, (self._room_id, str(danmaku.uname), str(danmaku.msg)))
                    await con.commit()
        await self._ws.send(dumps({
            'cmd': 'danmaku',
            'uname': danmaku.uname,
            'msg': danmaku.msg,
        }, ensure_ascii=False))

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        gift_id_list = core.config.get('blive_comment_api_gift_id_list', list, [])
        if str(gift.gift_id) not in gift_id_list:
            gift_id_list.append(str(gift.gift_id))
            core.config.set('gift_id_list', gift_id_list)
            await send_unknown_gift_mail(f'检测到未登记的礼物ID。 Name: {gift.gift_name}, ID: {gift.gift_id}',
                                         self._app.logger)
        if core.config.get('blive_comment_api_save_gifts', bool, False):
            async with self._app.mysql_pool.acquire() as con:
                async with con.cursor() as cur:
                    await cur.execute(insert_gift, (self._room_id, str(gift.uname), str(gift.gift_id),
                                                    str(gift.gift_name), str(gift.num), str(gift.coin_type),
                                                    str(gift.total_coin)))
                    await con.commit()
        await self._ws.send(dumps({
            'cmd': 'gift',
            'uname': gift.uname,
            'gift_name': gift.gift_name,
            'gift_id': gift.gift_id,
            'gift_num': gift.num,
            'coin_type': gift.coin_type,
            'total_coin': gift.total_coin,
        }, ensure_ascii=False))

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        await self._ws.send(dumps({
            'cmd': 'buy_guard',
            'uname': message.username,
            'guard_type': message.guard_level
        }, ensure_ascii=False))

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        await self._ws.send(dumps({
            'cmd': 'super_chat',
            'uname': message.uname,
            'msg': message.message,
            'price': message.price,
        }, ensure_ascii=False))

# -------------------------------------------------------------------------- DefaultBLiveClient --
