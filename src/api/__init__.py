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
from .server import run_server
from importlib import import_module
from .root_routes import *
from asyncio import get_event_loop

# -------------------------------------------------------------------------- Imports --

# -- Setup --------------------------------------------------------------------------

core.config.get('api_server_host', str, '0.0.0.0')
core.config.get('api_server_port', int, 5901)
core.config.get('api_server_access_log', bool, True)
core.config.get('api_server_debug', bool, False)
core.config.get('api_server_use_ipv6', bool, False)
core.config.get('api_server_worker_number', int, core.CPU_COUNT)

# -------------------------------------------------------------------------- Setup --

# -- Load API Extension --------------------------------------------------------------------------

for _extension in core.API_EXTENSION_DIR.iterdir():
    if _extension.is_dir():
        if _extension.joinpath('.is_active').is_file():
            try:
                import_module(f'src.api.extensions.{_extension.name}')
                get_event_loop().run_until_complete(
                    core.logger.save(f'Extension: {_extension.name[:-2]} loaded successfully.', core.logger.INFO)
                )
            except Exception as import_error:
                get_event_loop().run_until_complete(
                    core.logger.save(f'Extension: {_extension.name[:-2]} load failed. <Exception: {str(import_error)}>',
                                     core.logger.ERROR, True)
                )

# -------------------------------------------------------------------------- Load API Extension --

# -- Log --------------------------------------------------------------------------

get_event_loop().run_until_complete(
    core.logger.save("Loaded api-server module successfully.", core.logger.DEBUG)
)

# -------------------------------------------------------------------------- Log --
