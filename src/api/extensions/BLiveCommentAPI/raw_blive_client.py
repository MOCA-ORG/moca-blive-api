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

from . import blivedm
from aiohttp import ClientSession
from ujson import dumps
from ... import core

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

insert_raw_data = """
insert into raw_data(room_id, data) values (%s, %s);
"""

# -------------------------------------------------------------------------- Variables --

# -- RawBLiveClient --------------------------------------------------------------------------


class RawBLiveClient(blivedm.BLiveClient):

    def __init__(self, room_id, uid=0, session: ClientSession = None,
                 heartbeat_interval=30, ssl=True, loop=None, ws=None, app=None):
        super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)
        self._ws = ws
        self._app = app

    async def _handle_command(self, command):
        if isinstance(command, list):
            for one_command in command:
                await self._handle_command(one_command)
            return None
        else:
            raw_data = dumps(command, ensure_ascii=False)
            if core.config.get('blive_comment_api_save_raw_data', bool, False):
                async with self._app.mysql_pool.acquire() as con:
                    async with con.cursor() as cur:
                        await cur.execute(insert_raw_data, (str(self._room_id), raw_data))
                        await con.commit()
            await self._ws.send(raw_data)

# -------------------------------------------------------------------------- RawBLiveClient --
