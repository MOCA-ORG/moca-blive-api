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

from pathlib import Path
from moca_log import MocaLog, FileDriver
from moca_config import MocaConfig
from multiprocessing import cpu_count
from socket import gethostname, gethostbyname
from psutil import virtual_memory, swap_memory

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

TOP_DIR = Path(__file__).parent.parent.parent
LOG_DIR = TOP_DIR.joinpath('log')
SANIC_EXTENSION_DIR = TOP_DIR.joinpath('src').joinpath('sanic').joinpath('extensions')
API_EXTENSION_DIR = TOP_DIR.joinpath('src').joinpath('api').joinpath('extensions')

config: MocaConfig = MocaConfig('api_config', TOP_DIR, 'config.json', -1, debug_mode=False)

logger: MocaLog = MocaLog(FileDriver(LOG_DIR.joinpath('api.log')),
                          config.get('log_level', int, 1),
                          config.get('__debug__', bool, False))

CPU_COUNT: int = cpu_count()
HOST_NAME: str = gethostname()
HOST: str = gethostbyname(HOST_NAME)
MEMORY_SIZE: int = virtual_memory().total
SWAP_SIZE: int = swap_memory().total

# -------------------------------------------------------------------------- Variables --
