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

from typing import *
from ssl import SSLContext, Purpose, create_default_context
from .. import core

# -------------------------------------------------------------------------- Imports --

# -- SSLContext --------------------------------------------------------------------------


def create_ssl_context() -> Optional[SSLContext]:
    certfile: str = core.config.get('certfile', str, default='')
    keyfile: str = core.config.get('keyfile', str, default='')
    if certfile != '' and keyfile != '':
        ssl_context = create_default_context(Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=certfile,
                                    keyfile=keyfile)
    else:
        return None

# -------------------------------------------------------------------------- SSLContext --
