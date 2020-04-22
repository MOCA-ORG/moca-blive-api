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

from pymysql.err import MySQLError
from aiomysql import create_pool
from .. import core
from moca_log import MocaLog

# -------------------------------------------------------------------------- Imports --

# -- Create Pool --------------------------------------------------------------------------


async def create_aio_pool(logger: MocaLog,
                          host: str = '127.0.0.1',
                          port: int = 3306,
                          user: str = 'root',
                          password: str = '',
                          dbname: str = 'moca_system',
                          min_size: int = 1,
                          max_size: int = 10,
                          loop=None):
    """Create async connection pool. If some error occurred, return None."""
    try:
        pool = await create_pool(host=host,
                                 port=port,
                                 user=user,
                                 password=password,
                                 db=dbname,
                                 minsize=min_size,
                                 maxsize=max_size,
                                 loop=loop)
        await logger.save('get a async connection pool of mysql success.', logger.DEBUG)
        return pool
    except MySQLError as error:
        await logger.save('get a async connection pool of mysql failed.'
                          'Please check your user name, password and your database status.'
                          f'<MySQLError: {error}>', logger.DEBUG)
        return None


async def create_aio_pool_with_default_config(logger: MocaLog, loop=None):
    return await create_aio_pool(logger,
                                 core.config.get('mysql_host', str, '127.0.0.1'),
                                 core.config.get('mysql_port', int, 3306),
                                 core.config.get('mysql_user', str, 'root'),
                                 core.config.get('mysql_pass', str, ''),
                                 core.config.get('mysql_dbname', str, 'moca_system'),
                                 core.config.get('mysql_min_size', int, 1),
                                 core.config.get('mysql_max_size', int, 10),
                                 loop)
# -------------------------------------------------------------------------- Create Pool --
