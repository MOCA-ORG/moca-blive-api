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

from src.moca_modules.moca_sanic import MocaSanic
from ssl import SSLContext
from sanic import Sanic
from src.moca_modules.moca_config import MocaFileConfig
from src.moca_modules.moca_log import MocaAsyncFileLog
from src.moca_modules.moca_utils import *
from src.moca_modules.moca_mysql import MocaMysql
from src.moca_modules.moca_redis import MocaRedis
from pathlib import Path
from src.core import LOG_DIR, TOP_DIR, VERSION
from src.database import comments_table, gifts_table
from pymysql import Warning
from warnings import filterwarnings

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

filterwarnings('ignore', category=Warning)

# -------------------------------------------------------------------------- Init --

# -- API Server --------------------------------------------------------------------------


class MocaBliveAPIServer(MocaSanic):
    """
    The Bilibili live API Server
    """

    def __init__(self, name: str, host: str, port: int, ssl: Optional[SSLContext] = None,
                 log_dir: Optional[Union[str, Path]] = None, internal_key_file: Optional[Union[str, Path]] = None,
                 access_log: bool = False, use_ipv6: bool = False, workers: int = 0, headers: dict = {}):
        """
        :param name: the name of the sanic server.
        :param host: the host address of the sanic server.
        :param port: the port of the sanic server.
        :param ssl: the ssl context of the sanic server.
        :param log_dir: the directory path of the logs.
        :param internal_key_file: the internal key file path. (the content of internal key file must be 1024 characters)
        :param access_log: logging access.
        :param use_ipv6: use ipv6
        :param workers: the number of workers,
                        if workers is 0, the workers number will be same to the number of cpu cores.
        :param headers: the response headers.
        """
        super().__init__(name, host, port, ssl, log_dir, internal_key_file, access_log, use_ipv6, workers, headers)

    @staticmethod
    async def before_server_start(app: Sanic, loop):
        set_process_name(f'MocaBliveAPI - Server Instances - {current_process().pid}')
        app.moca_config: MocaFileConfig = MocaFileConfig(TOP_DIR.joinpath('config.json'))
        app.moca_log: MocaAsyncFileLog = MocaAsyncFileLog(
            LOG_DIR.joinpath('usage.log'), LOG_DIR.joinpath('error.log'),
            log_rotate=app.moca_config.get('log_rotate', False)
        )
        await app.moca_log.init()
        app.mysql: MocaMysql = MocaMysql(
            app.moca_config.get('mysql_host', '127.0.0.1'),
            app.moca_config.get('mysql_port', 3306),
            app.moca_config.get('mysql_user', 'root'),
            app.moca_config.get('mysql_pass', 'pass'),
            app.moca_config.get('mysql_db', 'moca_blive_api'),
        )
        app.redis: MocaRedis = MocaRedis(
            app.moca_config.get('redis_host', '127.0.0.1'),
            app.moca_config.get('redis_port', 6379),
            app.moca_config.get('redis_db_index', 0),
            app.moca_config.get('redis_pass', 'pass'),
        )
        try:
            pool = await app.mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(comments_table)
                    await cursor.execute(gifts_table)
                    await con.commit()
        except Warning:
            pass

    @staticmethod
    async def after_server_start(app: Sanic, loop):
        print(f"MocaBliveAPI服务器({VERSION})启动成功。<Process: {current_process().pid}>")

# -------------------------------------------------------------------------- API Server --
