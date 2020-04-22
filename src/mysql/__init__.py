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
from .get_con import get_con, get_con_with_default_config, get_aio_con, get_aio_con_with_default_config
from .create_pool import create_aio_pool, create_aio_pool_with_default_config
from asyncio import get_event_loop

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

mysql_con = get_con_with_default_config()

# -------------------------------------------------------------------------- Variables --

# -- Init --------------------------------------------------------------------------

core.config.get('mysql_host', str, '127.0.0.1')
core.config.get('mysql_port', int, 3306)
core.config.get('mysql_user', str, 'root')
core.config.get('mysql_pass', str, '')
core.config.get('mysql_dbname', str, 'blive_comment_api')
core.config.get('mysql_min_size', int, 1)
core.config.get('mysql_max_size', int, 10)

# -------------------------------------------------------------------------- Init --

# -- Log --------------------------------------------------------------------------

get_event_loop().run_until_complete(
    core.logger.save("Loaded mysql module successfully.", core.logger.DEBUG)
)

# -------------------------------------------------------------------------- Log --
