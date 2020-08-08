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
from typing import *
from ujson import dumps
from src.moca_modules.moca_config import MocaFileConfig
from sanic import Sanic
from sanic.websocket import WebSocketConnection

# -------------------------------------------------------------------------- Imports --

# -- RawBLiveClient --------------------------------------------------------------------------


class RawBLiveClient(blivedm.BLiveClient):

    def __init__(self, room_id: str, ws: WebSocketConnection, app: Sanic, config: MocaFileConfig):
        super().__init__(room_id)
        self._ws = ws
        self._app = app
        self._config = config

    async def _handle_command(self, command):
        if isinstance(command, list):
            for one_command in command:
                await self._handle_command(one_command)
            return None
        else:
            raw_data = dumps(command, ensure_ascii=False)
            await self._ws.send(raw_data)

# -------------------------------------------------------------------------- RawBLiveClient --
