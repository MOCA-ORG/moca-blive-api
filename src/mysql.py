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
from aiomysql import connect
from .core import moca_config, loop
from .save_log import save_log

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('mysql_host', str, '127.0.0.1')
moca_config.get('mysql_port', int, 3306)
moca_config.get('mysql_user', str, 'root')
moca_config.get('mysql_pass', str, '')
moca_config.get('mysql_dbname', str, 'blive_comment_api')

# -------------------------------------------------------------------------- Init --

# -- Get Connection --------------------------------------------------------------------------


async def get_aio_con(host: str = '127.0.0.1',
                      port: int = 3306,
                      user: str = 'root',
                      password: str = '',
                      dbname: str = 'blive_comment_api'):
    """如果获取连接失败，返回None"""
    try:
        con = await connect(host=host,
                            port=port,
                            user=user,
                            password=password,
                            db=dbname,
                            loop=loop)
        return con
    except MySQLError as error:
        await save_log('异步的mysql数据库连接获取失败。'
                       '请确认您的用户名和密码是否正确，请确认您的数据库的状态。'
                       '<MySQLError: %s>' % str(error))
        return None


async def get_aio_con_with_default_config():
    """如果获取连接失败，返回None"""
    return await get_aio_con(host=moca_config.get('mysql_host', str, '127.0.0.1'),
                             port=moca_config.get('mysql_port', int, 3306),
                             user=moca_config.get('mysql_user', str, 'root'),
                             password=moca_config.get('mysql_pass', str, ''),
                             dbname=moca_config.get('mysql_dbname', str, 'blive_comment_api'))

# -------------------------------------------------------------------------- Get Connection --
