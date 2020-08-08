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


# -- Init --------------------------------------------------------------------------
from subprocess import call
from sys import executable
from pathlib import Path
from multiprocessing import current_process

# Check modules
try:
    from apsw import Connection
except (ModuleNotFoundError, ImportError):
    # install apsw module
    call(
        f"{executable} -m pip install --user https://github.com/rogerbinns/apsw/releases/download/3.32.2-r1/"
        f"apsw-3.32.2-r1.zip --global-option=fetch --global-option=--version --global-option=3.32.2 --global"
        f"-option=--all --global-option=build --global-option=--enable-all-extensions",
        shell=True
    )

try:
    from . import (
        moca_base_class, moca_file, moca_log, moca_utils, moca_variables, moca_config, moca_mail, moca_redis,
        moca_encrypt, moca_memory, moca_random, moca_sanic, moca_core_db, moca_console, moca_level_db, moca_users,
        moca_sms, moca_access,
    )
except (ModuleNotFoundError, ImportError):
    with open(str(Path(__file__).parent.joinpath('requirements.txt')), mode='r', encoding='utf-8') as __require_file:
        __requirements = __require_file.read().splitlines()
    call(f"{executable} -m pip install --upgrade pip {' '.join(__requirements)}", shell=True)
    del __requirements, __require_file
    from . import (
        moca_base_class, moca_file, moca_log, moca_utils, moca_variables, moca_config, moca_mail, moca_redis,
        moca_encrypt, moca_memory, moca_random, moca_sanic, moca_core_db, moca_console, moca_level_db, moca_users,
        moca_sms, moca_access,
    )

# Write PID file.
with open(str(Path(__file__).parent.joinpath('storage').joinpath('moca.pid')), mode='w', encoding='utf-8') as __fp:
    __fp.write(str(current_process().pid))

# -------------------------------------------------------------------------- Init --
