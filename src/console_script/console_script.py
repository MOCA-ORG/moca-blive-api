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

from docopt import docopt
from src.core import moca_log, VERSION, moca_config, LOG_DIR
from src.moca_modules.moca_variables import LICENSE
from src.moca_modules.moca_utils import print_warning, print_error, set_process_name
from time import sleep
from src.server import server
from asyncio import get_event_loop
from src.blive_api import DefaultBLiveClient
from src.moca_modules.moca_mysql import MocaMysql
from src.moca_modules.moca_redis import MocaRedis
from src.moca_modules.moca_log import MocaAsyncFileLog
from multiprocessing import current_process

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

__doc__ = f"""

Welcome to MocaSystem(MocaBliveAPI).

Usage:
    moca.py run
    moca.py run-listener <room_id>
    moca.py --license
    moca.py --version
    moca.py --tako
"""

# -------------------------------------------------------------------------- Variables --

# -- Console Script --------------------------------------------------------------------------


def console_script():
    try:
        args = docopt(__doc__)
        if args['--license']:
            print(LICENSE)
        elif args['--version']:
            print(VERSION)
        elif args['--tako']:
            for _ in range(10):
                print('いあ！いあ！めんだこちゃん！ふたぐん!')
                sleep(0.2)
            print('https://twitter.com/Mendako_Vtuber')
        elif args['run']:
            server.run_server(True)
        elif args['run-listener']:
            room_id = str(args['<room_id>'])
            set_process_name(f'MocaBliveAPI - Room Listener - {room_id}')
            redis = MocaRedis(
                moca_config.get('redis_host', '127.0.0.1'),
                moca_config.get('redis_port', 6379),
                moca_config.get('redis_db_index', 0),
                moca_config.get('redis_pass', 'pass'),
            )
            get_event_loop().run_until_complete(redis.save('moca-blive-api-pid-' + room_id, current_process().pid))
            client = DefaultBLiveClient(
                str(room_id),
                MocaMysql(
                    moca_config.get('mysql_host', '127.0.0.1'),
                    moca_config.get('mysql_port', 3306),
                    moca_config.get('mysql_user', 'root'),
                    moca_config.get('mysql_pass', 'pass'),
                    moca_config.get('mysql_db', 'moca_blive_api'),
                ),
                redis,
                moca_config,
                MocaAsyncFileLog(
                    LOG_DIR.joinpath('usage.log'), LOG_DIR.joinpath('error.log'),
                    log_rotate=moca_config.get('log_rotate', False)
                )
            )
            try:
                get_event_loop().run_until_complete(client.start())
            finally:
                get_event_loop().run_until_complete(client.close())
        else:
            print_warning("未知命令。")
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as error:
        error_str = f"发生未知异常。 <Exception: {error}>"
        print_error(error_str)
        moca_log.save(error_str, moca_log.LogLevel.ERROR)

# -------------------------------------------------------------------------- Console Script --
