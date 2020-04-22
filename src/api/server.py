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

from ..sanic import run_websocket_server
from .. import core
from multiprocessing import current_process
from moca_log import MocaLog, FileDriver
from .app import app
from ..mysql import create_aio_pool_with_default_config
from ..ssl import create_ssl_context

# -------------------------------------------------------------------------- Imports --

# -- Add Blueprints --------------------------------------------------------------------------

# -------------------------------------------------------------------------- Add Blueprints --

# -------------------------------------------------------------------------- Set Listener --


@app.listener('before_server_start')
async def before_server_start(app_, loop):
    """Sanic Listener"""
    # Setup logger
    app_.logger = MocaLog(FileDriver(core.LOG_DIR.joinpath('api.log')),
                          core.config.get('log_level', int, 1),
                          core.config.get('__debug__', bool, False))

    # Setup mysql connection pool
    app_.mysql_pool = await create_aio_pool_with_default_config(app_.logger, loop)

    await app_.logger.save(f'API Server is starting. [{current_process().name}]', core.logger.DEBUG)


@app.listener('after_server_start')
async def after_server_start(app_, loop):
    """Sanic Listener"""
    await app_.logger.save(f'API Server is started. [{current_process().name}]', core.logger.DEBUG)


@app.listener('before_server_stop')
async def before_server_stop(app_, loop):
    """Sanic Listener"""
    await app_.logger.save(f'API Server is stopping. [{current_process().name}]', core.logger.DEBUG)


@app.listener('after_server_stop')
async def after_server_stop(app_, loop):
    """Sanic Listener"""
    if app_.mysql_pool is not None:
        app_.mysql_pool.close()
    await app_.logger.save(f'API Server is stopped. [{current_process().name}]', core.logger.DEBUG)


# -------------------------------------------------------------------------- Set Listener --

# -- Run --------------------------------------------------------------------------


def run_server():
    run_websocket_server(app,
                         create_ssl_context(),
                         core.config.get('api_server_host', str, '0.0.0.0'),
                         core.config.get('api_server_port', int, 7899),
                         core.config.get('api_server_access_log', bool, True),
                         core.config.get('api_server_debug', bool, False),
                         core.config.get('api_server_use_ipv6', bool, False),
                         core.config.get('api_server_worker_number', int, core.CPU_COUNT))

# -------------------------------------------------------------------------- Run --
