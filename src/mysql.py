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


# -- Imports --------------------------------------------------------------------------

from pymysql.err import MySQLError
from aiomysql import create_pool
from .core import moca_config
from .save_log import save_log
from moca_core import os_exit

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('mysql_host', str, '127.0.0.1')
moca_config.get('mysql_port', int, 3306)
moca_config.get('mysql_user', str, 'root')
moca_config.get('mysql_pass', str, '')
moca_config.get('mysql_dbname', str, 'blive_comment_api')
moca_config.get('mysql_minsize', int, 1)
moca_config.get('mysql_maxsize', int, 10)

# -------------------------------------------------------------------------- Init --

# -- Get Connection --------------------------------------------------------------------------


async def get_aio_con_pool(host: str = '127.0.0.1',
                           port: int = 3306,
                           user: str = 'root',
                           password: str = '',
                           dbname: str = 'blive_comment_api',
                           minsize: int = 1,
                           maxsize: int = 10):
    """如果获取连接失败，返回None"""
    try:
        con = await create_pool(host=host,
                                port=port,
                                user=user,
                                password=password,
                                db=dbname,
                                maxsize=maxsize,
                                minsize=minsize)
        return con
    except MySQLError as error:
        save_log('异步的mysql数据库连接获取失败。'
                 '请确认您的用户名和密码是否正确，请确认您的数据库的状态。'
                 '<MySQLError: %s>' % str(error))
        os_exit(1, '连接数据库失败。')
        return None


async def get_aio_con_pool_with_default_config():
    """如果获取连接失败，返回None"""
    return await get_aio_con_pool(host=moca_config.get('mysql_host', str, '127.0.0.1'),
                                  port=moca_config.get('mysql_port', int, 3306),
                                  user=moca_config.get('mysql_user', str, 'root'),
                                  password=moca_config.get('mysql_pass', str, ''),
                                  dbname=moca_config.get('mysql_dbname', str, 'blive_comment_api'),
                                  minsize=moca_config.get('mysql_minsize', int, 1),
                                  maxsize=moca_config.get('mysql_maxsize', int, 10))

# -------------------------------------------------------------------------- Get Connection --
