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

from pymysql import Connection
from pymysql.err import MySQLError
from aiomysql import connect
from .. import core
from asyncio import get_event_loop
from moca_log import MocaLog

# -------------------------------------------------------------------------- Imports --

# -- Get Connection --------------------------------------------------------------------------


def get_con(host: str = '127.0.0.1',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            dbname: str = 'moca_system'):
    """If can't get database connection return None."""
    try:
        con = Connection(host=host,
                         port=port,
                         user=user,
                         password=password,
                         db=dbname)
        get_event_loop().run_until_complete(
            core.logger.save('get a connection of mysql success', core.logger.DEBUG)
        )
        return con
    except MySQLError as error:
        get_event_loop().run_until_complete(
            core.logger.save('get a connection of mysql failed.'
                             'Please check your user name, password and your database status.'
                             f'<MySQLError: {error}>', core.logger.ERROR, True)
        )
        return None


def get_con_with_default_config():
    """If can't get database connection return None."""
    return get_con(host=core.config.get('mysql_host', str, '127.0.0.1'),
                   port=core.config.get('mysql_port', int, 3306),
                   user=core.config.get('mysql_user', str, 'root'),
                   password=core.config.get('mysql_pass', str, ''),
                   dbname=core.config.get('mysql_dbname', str, 'moca_system'))


async def get_aio_con(logger: MocaLog,
                      host: str = '127.0.0.1',
                      port: int = 3306,
                      user: str = 'root',
                      password: str = '',
                      dbname: str = 'moca_system'):
    """If can't get database connection return None."""
    try:
        con = await connect(host=host,
                            port=port,
                            user=user,
                            password=password,
                            db=dbname)
        await logger.save('get a async connection of mysql success.', logger.DEBUG)
        return con
    except MySQLError as error:
        await logger.save('get a async connection of mysql failed.'
                          'Please check your user name, password and your database status.'
                          f'<MySQLError: {error}>', logger.DEBUG)
        return None


async def get_aio_con_with_default_config(logger: MocaLog):
    """If can't get database connection return None."""
    return await get_aio_con(logger,
                             host=core.config.get('mysql_host', str, '127.0.0.1'),
                             port=core.config.get('mysql_port', int, 3306),
                             user=core.config.get('mysql_user', str, 'root'),
                             password=core.config.get('mysql_pass', str, ''),
                             dbname=core.config.get('mysql_dbname', str, 'moca_system'))

# -------------------------------------------------------------------------- Get Connection --
