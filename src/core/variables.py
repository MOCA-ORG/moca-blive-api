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

from src.moca_modules.moca_config import MocaFileConfig
from src.moca_modules.moca_log import MocaFileLog
from pathlib import Path

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

VERSION: str = '1.1.0'

TOP_DIR: Path = Path(__file__).parent.parent.parent
LOG_DIR: Path = TOP_DIR.joinpath('log')
LOG_DIR.mkdir(parents=True, exist_ok=True)

moca_config: MocaFileConfig = MocaFileConfig(TOP_DIR.joinpath('config.json'))

moca_log: MocaFileLog = MocaFileLog(
    LOG_DIR.joinpath('usage.log'), LOG_DIR.joinpath('error.log'), log_rotate=moca_config.get('log_rotate', False)
)

# -------------------------------------------------------------------------- Variables --
