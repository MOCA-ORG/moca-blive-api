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

from ... import core
from ....email import send_aio_notification_mail
from moca_log import MocaLog

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

core.config.get('blive_comment_api_send_mail_if_found_unknown_gift_name', bool, False)
core.config.get('blive_comment_api_send_mail_if_start_listen', bool, False)
core.config.get('blive_comment_api_send_mail_if_stop_listen', bool, False)

# -------------------------------------------------------------------------- Init --

# -- Send Mail --------------------------------------------------------------------------


async def send_unknown_gift_mail(message: str, logger: MocaLog) -> bool:
    if core.config.get('blive_comment_api_send_mail_if_found_unknown_gift_name', bool, False):
        return await send_aio_notification_mail(message, logger)
    else:
        return True


async def send_start_listen_mail(message: str, logger: MocaLog) -> bool:
    if core.config.get('blive_comment_api_send_mail_if_start_listen', bool, False):
        return await send_aio_notification_mail(message, logger)
    else:
        return True


async def send_stop_listen_mail(message: str, logger: MocaLog) -> bool:
    if core.config.get('blive_comment_api_send_mail_if_stop_listen', bool, False):
        return await send_aio_notification_mail(message, logger)
    else:
        return True

# -------------------------------------------------------------------------- Send Mail --
