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


# -- Imports --------------------------------------------------------------------------

from .send_mail import send_mail
from . import blivedm
from aiohttp import ClientSession
from ujson import dumps
from .core import moca_config

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('gift_id_list', list, [])

# -------------------------------------------------------------------------- Init --

insert_gift = """
insert into user_gifts(room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin) 
values(%s, %s, %s, %s, %s, %s, %s);
"""

insert_comment = """
insert into user_comments(room_id, user_name, comment) 
values(%s, %s, %s);
"""

# -- MyBLiveClient --------------------------------------------------------------------------


class MyBLiveClient(blivedm.BLiveClient):
    # 自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    def __init__(self, room_id, uid=0, session: ClientSession = None,
                 heartbeat_interval=30, ssl=True, loop=None, ws=None, app=None):
        super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)
        self._ws = ws
        self._app = app

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        async with self._app.pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(insert_comment, (self._room_id, str(danmaku.uname), str(danmaku.msg)))
                await con.commit()
        await self._ws.send(dumps({
            'cmd': 'danmaku',
            'uname': danmaku.uname,
            'msg': danmaku.msg,
        }, ensure_ascii=False))

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        gift_id_list = moca_config.get('gift_id_list', list, [])
        if str(gift.gift_id) not in gift_id_list:
            gift_id_list.append(str(gift.gift_id))
            moca_config.set('gift_id_list', gift_id_list)
            await send_mail(f'检测到未登记的礼物ID。 Name: {gift.gift_name}, ID: {gift.gift_id}')
        async with self._app.pool.acquire() as con:
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

# -------------------------------------------------------------------------- MyBLiveClient --
