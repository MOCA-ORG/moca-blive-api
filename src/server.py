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

from socket import AF_INET6, SOCK_STREAM, socket
from sanic import Sanic
from moca_core import get_random_string
from sanic.response import text, json
from pathlib import Path
from sanic.websocket import WebSocketProtocol
from .core import moca_config
from warnings import filterwarnings
from .save_log import save_log
from moca_core import get_process_id
import ssl
from sanic.log import logger, LOGGING_CONFIG_DEFAULTS
from logging import INFO
from .default_blive_client import DefaultBLiveClient
from .raw_blive_client import RawBLiveClient
from ujson import loads
from .mysql import get_aio_con_pool_with_default_config
from pymysql import Warning
from .send_mail import send_start_listen_mail, send_stop_listen_mail
from .blivedm import InitError

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

filterwarnings("error", category=Warning)

moca_config.get('api_server_host', str, '0.0.0.0')
moca_config.get('api_key', str, get_random_string(64))
moca_config.get('api_server_port', int, 7899)
moca_config.get('api_server_use_ssl', bool, False)
moca_config.get('api_server_certfile', str, '')
moca_config.get('api_server_keyfile', str, '')
moca_config.get('api_server_access_log', bool, False)
moca_config.get('api_server_debug', bool, False)
moca_config.get('api_server_use_ipv6', bool, False)

moca_config.get('save_gifts', bool, False)
moca_config.get('save_comments', bool, False)
moca_config.get('save_raw_data', bool, False)

# -------------------------------------------------------------------------- Init --

# -- Setup Log --------------------------------------------------------------------------

logger.setLevel(INFO)

LOGGING_CONFIG_DEFAULTS['handlers']['root_file'] = {
    'class': 'logging.FileHandler',
    'formatter': 'generic',
    'filename': str(Path(__file__).parent.parent.joinpath('log').joinpath('sanic_root.log'))
}
LOGGING_CONFIG_DEFAULTS['handlers']['error_file'] = {
    'class': 'logging.FileHandler',
    'formatter': 'generic',
    'filename': str(Path(__file__).parent.parent.joinpath('log').joinpath('sanic_error.log'))
}
LOGGING_CONFIG_DEFAULTS['handlers']['access_file'] = {
    'class': 'logging.FileHandler',
    'formatter': 'access',
    'filename': str(Path(__file__).parent.parent.joinpath('log').joinpath('sanic_access.log'))
}
LOGGING_CONFIG_DEFAULTS['loggers']['sanic.root']['handlers'][0] = 'root_file'
LOGGING_CONFIG_DEFAULTS['loggers']['sanic.error']['handlers'][0] = 'error_file'
LOGGING_CONFIG_DEFAULTS['loggers']['sanic.access']['handlers'][0] = 'access_file'

# -------------------------------------------------------------------------- Setup Log --

# -- Variables --------------------------------------------------------------------------

app: Sanic = Sanic('BliveCommentAPI')

online_list: list = []

gifts_table = """
create table if not exists user_gifts (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    user_name varchar(64) not null,
    gift_id varchar(16) not null,
    gift_name varchar(16) not null,
    gift_num varchar(16) not null, 
    coin_type varchar(16) not null,
    total_coin varchar(16) not null
); 
"""

comments_table = """
create table if not exists user_comments (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    user_name varchar(64) not null,
    comment varchar(128) not null 
); 
"""

raw_table = """
create table if not exists raw_data (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    data TEXT not null
); 
"""

# -------------------------------------------------------------------------- Variables --

# -- Websocket --------------------------------------------------------------------------


@app.route('/status', methods={'GET', 'POST', 'OPTIONS'})
async def status(request):
    return text('BliveCommentAPI is running.')


@app.route('/online', methods={'GET', 'POST', 'OPTIONS'})
async def online(request):
    return json(online_list)


@app.websocket('/live')
async def live(request, ws):
    data = loads(await ws.recv())
    if data['cmd'] == 'start' and data['api_key'] == moca_config.get('api_key', str, ''):
        if data['room_id'] not in online_list:
            online_list.append(data['room_id'])
        client = DefaultBLiveClient(room_id=data['room_id'], loop=app.loop, ws=ws, app=app)
        try:
            save_log(f"开始监听直播: {data['room_id']}")
            await send_start_listen_mail(f"开始监听直播: {data['room_id']}")
            await client.start()
        except InitError:
            await ws.send('ROOM ID ERROR')
        finally:
            online_list.remove(data['room_id'])
            save_log(f"停止监听直播: {data['room_id']}")
            await send_stop_listen_mail(f"停止监听直播: {data['room_id']}")
            await client.close()
    else:
        await ws.send('API KEY ERROR')


@app.websocket('/raw')
async def live(request, ws):
    data = loads(await ws.recv())
    if data['cmd'] == 'start' and data['api_key'] == moca_config.get('api_key', str, ''):
        if data['room_id'] not in online_list:
            online_list.append(data['room_id'])
        client = RawBLiveClient(room_id=data['room_id'], loop=app.loop, ws=ws, app=app)
        try:
            save_log(f"开始监听直播: {data['room_id']}")
            await send_start_listen_mail(f"开始监听直播: {data['room_id']}")
            await client.start()
        except InitError:
            await ws.send('ROOM ID ERROR')
        finally:
            online_list.remove(data['room_id'])
            save_log(f"停止监听直播: {data['room_id']}")
            await send_stop_listen_mail(f"停止监听直播: {data['room_id']}")
            await client.close()
    else:
        await ws.send('API KEY ERROR')

# -------------------------------------------------------------------------- Websocket --

# -------------------------------------------------------------------------- Set Listener --


@app.listener('before_server_start')
async def before_server_start(app_, loop):
    if moca_config.get('save_comments', bool, False) or \
            moca_config.get('save_gifts', bool, False) or \
            moca_config.get('save_raw_data', bool, False):
        app_.pool = await get_aio_con_pool_with_default_config()
        try:
            if moca_config.get('save_comments', bool, False):
                async with app_.pool.acquire() as con:
                    async with con.cursor() as cur:
                        await cur.execute(comments_table)
                        await con.commit()
        except Warning:
            pass
        try:
            if moca_config.get('save_gifts', bool, False):
                async with app_.pool.acquire() as con:
                    async with con.cursor() as cur:
                        await cur.execute(gifts_table)
                        await con.commit()
        except Warning:
            pass
        try:
            if moca_config.get('save_raw_data', bool, False):
                async with app_.pool.acquire() as con:
                    async with con.cursor() as cur:
                        await cur.execute(raw_table)
                        await con.commit()
        except Warning:
            pass
    else:
        app_.pool = None

# --------------------------------------------------------------------------Set Listener --

# -- Run Server --------------------------------------------------------------------------


def run_server() -> None:
    try:
        if moca_config.get('api_server_use_ssl', bool, False):
            if moca_config.get('api_server_certfile', str, '') == '':
                save_log('[SSL]无法获取必要设定信息。 <certfile>')
                ssl_context = None
            elif moca_config.get('api_server_keyfile', str, '') == '':
                save_log('[SSL]无法获取必要设定信息。 <keyfile>')
                ssl_context = None
            elif not Path(moca_config.get('api_server_certfile', str, '')).is_file():
                save_log('[SSL]文件地址异常。无法找到文件。 <certfile>')
                ssl_context = None
            elif not Path(moca_config.get('api_server_keyfile', str, '')).is_file():
                save_log('[SSL]文件地址异常。无法找到文件。 <keyfile>')
                ssl_context = None
            else:
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(certfile=moca_config.get('api_server_certfile', str, ''),
                                            keyfile=moca_config.get('api_server_keyfile', str, ''))
        else:
            ssl_context = None
        host: str = moca_config.get('api_server_host', str, '0.0.0.0')
        port: int = moca_config.get('api_server_port', int, 7899)
        print('服务器信息。 host: %s, port: %s' % (host, port))
        moca_config.set('__pid__', get_process_id())
        moca_config.set('__server_is_running__', True)
        if moca_config.get('api_server_use_ipv6', bool, False):
            sock = socket(AF_INET6, SOCK_STREAM)
            sock.bind((host, port))
            app.run(sock=sock,
                    access_log=moca_config.get('api_server_access_log', bool, False),
                    ssl=ssl_context,
                    debug=moca_config.get('api_server_debug', bool, False),
                    workers=1,
                    protocol=WebSocketProtocol)
        else:
            app.run(host=host,
                    port=port,
                    access_log=moca_config.get('api_server_access_log', bool, False),
                    ssl=ssl_context,
                    debug=moca_config.get('api_server_debug', bool, False),
                    workers=1,
                    protocol=WebSocketProtocol)
    except OSError as os_error:
        print('API服务器停止运行，请检查您的端口是否可以使用。 <OSError: %s>' % str(os_error))
    except Exception as other_error:
        print('API服务器停止运行，发生未知异常。 <Exception: %s>' % str(other_error))
    finally:
        if moca_config.get('api_server_use_ipv6', bool, False):
            sock.close()
        moca_config.set('__server_is_running__', False)
        moca_config.set('__pid__', 0)


# -------------------------------------------------------------------------- Run Server --
