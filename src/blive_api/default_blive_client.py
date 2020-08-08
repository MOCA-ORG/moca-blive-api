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

from . import blivedm
from src.core import moca_config
from src.moca_modules.moca_config import MocaFileConfig
from src.moca_modules.moca_redis import MocaRedis
from src.moca_modules.moca_mysql import MocaMysql
from src.moca_modules.moca_log import MocaAsyncFileLog
from src.database import save_gift, save_comment

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

if moca_config.get('blive_comment_api_gift_id_list', None) is None:
    moca_config.set('blive_comment_api_gift_id_list', ["1", "3", "25", "7", "8", "39", "20003", "20004", "20008",
                                                       "20014", "30004", "30046", "30063", "30064", "30072", "30087",
                                                       "30090", "30135", "30136", "30143", "30144", "30145", "30204",
                                                       "550001", "550002", "550003", "550004", "550005", "30205",
                                                       "20002", "30508"])

# -------------------------------------------------------------------------- Init --

# -- DefaultBLiveClient --------------------------------------------------------------------------


class DefaultBLiveClient(blivedm.BLiveClient):

    def __init__(self, room_id: str, mysql: MocaMysql, redis: MocaRedis, config: MocaFileConfig, log: MocaAsyncFileLog):
        super().__init__(room_id)
        self._room_id = room_id
        self._redis = redis
        self._mysql = mysql
        self._config = config
        self._log = log

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        pool = await self._mysql.get_aio_pool()
        await save_comment(pool, self._room_id, danmaku.uname, danmaku.msg)
        await self._redis.rpush(
            'moca-blive-api-' + str(self._room_id),
            {
                'cmd': 'danmaku',
                'uname': danmaku.uname,
                'msg': danmaku.msg,
            }
        )

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        gift_id_list = self._config.get('blive_comment_api_gift_id_list', [])
        if str(gift.gift_id) not in gift_id_list:
            gift_id_list.append(str(gift.gift_id))
            self._config.set('blive_comment_api_gift_id_list', gift_id_list)
            await self._log.save(f'检测到未登记的礼物ID。 Name: {gift.gift_name}, ID: {gift.gift_id}', 1)
        pool = await self._mysql.get_aio_pool()
        await save_gift(
            pool, self._room_id, gift.uname, gift.gift_id, gift.gift_name, gift.num, gift.coin_type, gift.total_coin
        )
        await self._redis.rpush(
            'moca-blive-api-' + str(self._room_id),
            {
                'cmd': 'gift',
                'uname': gift.uname,
                'gift_name': gift.gift_name,
                'gift_id': gift.gift_id,
                'gift_num': gift.num,
                'coin_type': gift.coin_type,
                'total_coin': gift.total_coin,
            }
        )

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        await self._redis.rpush(
            'moca-blive-api-' + str(self._room_id),
            {
                'cmd': 'buy_guard',
                'uname': message.username,
                'guard_type': message.guard_level
            }
        )

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        await self._redis.rpush(
            'moca-blive-api-' + str(self._room_id),
            {
                'cmd': 'super_chat',
                'uname': message.uname,
                'msg': message.message,
                'price': message.price,
            }
        )

# -------------------------------------------------------------------------- DefaultBLiveClient --
