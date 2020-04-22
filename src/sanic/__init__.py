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

from .. import core
from importlib import import_module
from asyncio import get_event_loop
from .run_http_server import run_http_server
from .run_websocket_server import run_websocket_server
from .setup_logging import setup_logging
from .utils import *

# -------------------------------------------------------------------------- Imports --

# -- Load Websocket Extension --------------------------------------------------------------------------

for _extension in core.SANIC_EXTENSION_DIR.iterdir():
    if _extension.is_dir():
        if _extension.joinpath('.is_active').is_file():
            try:
                import_module(f'src.server.sanic.extensions.{_extension.name}')
                get_event_loop().run_until_complete(
                    core.logger.save(f'Extension: {_extension.name[:-2]} loaded successfully.', core.logger.INFO)
                )
            except Exception as import_error:
                get_event_loop().run_until_complete(
                    core.logger.save(f'Extension: {_extension.name[:-2]} load failed. <Exception: {str(import_error)}>',
                                     core.logger.ERROR, True)
                )

# -------------------------------------------------------------------------- Load Websocket Extension --

# -- Log --------------------------------------------------------------------------

get_event_loop().run_until_complete(
    core.logger.save("Loaded websocket-server module successfully.", core.logger.DEBUG)
)

# -------------------------------------------------------------------------- Log --
