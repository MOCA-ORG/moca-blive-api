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

from .. import core
from typing import Optional
from ssl import SSLContext
from sanic import Sanic
from socket import AF_INET6, SOCK_STREAM, socket
from sanic.websocket import WebSocketProtocol

# -------------------------------------------------------------------------- Imports --

# -- Run --------------------------------------------------------------------------


def run_websocket_server(app: Sanic,
                         ssl: Optional[SSLContext],
                         host: str,
                         port: int,
                         access_log: bool = False,
                         debug: bool = False,
                         use_ipv6: bool = False,
                         workers=1) -> None:
    """Run Sanic server."""
    try:
        if use_ipv6:
            sock = socket(AF_INET6, SOCK_STREAM)
            sock.bind((host, port))
            app.run(sock=sock,
                    access_log=access_log,
                    ssl=ssl,
                    debug=debug,
                    workers=workers,
                    protocol=WebSocketProtocol)
        else:
            app.run(host=host,
                    port=port,
                    access_log=access_log,
                    ssl=ssl,
                    debug=debug,
                    workers=workers,
                    protocol=WebSocketProtocol)
    except OSError as os_error:
        core.print_warning(f'Sanic Websocket Server stopped. Please check your port is usable. <OSError: {os_error}>')
    except Exception as other_error:
        core.print_warning(f'Sanic Websocket Server stopped, unknown error occurred. <Exception: {other_error}>')
    finally:
        if use_ipv6:
            sock.close()

# -------------------------------------------------------------------------- Run --
