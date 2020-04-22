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

from .send import *
from traceback import format_exc
from .. import core
from asyncio import get_event_loop

# -------------------------------------------------------------------------- Imports --

# -- Setup --------------------------------------------------------------------------

core.config.get('smtp_use_ssl', bool, True)
core.config.get('smtp_host', str, '')
core.config.get('smtp_port', int, 465)
core.config.get('smtp_notification_user', str, '')
core.config.get('smtp_notification_pass', str, '')
core.config.get('smtp_notification_from_address', str, '')
core.config.get('smtp_notification_to_address', list, [''])


async def _error_event(message, *args, **kwargs):
    body = f"""
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Error Occurred!!</h1>
    <h3>{message}</h3>
    <hr>
    <hr>
    <pre>
    {format_exc()}
    </pre>
    <hr>
    <hr>
</body>
</html>
    """
    await send_aio_notification_mail(body)

if core.config.get('send_notification_when_critical_error_occurred', bool, False):
    core.logger.add_handler(core.logger.CRITICAL, _error_event)
if core.config.get('send_notification_when_error_occurred', bool, False):
    core.logger.add_handler(core.logger.ERROR, _error_event)

# -------------------------------------------------------------------------- Setup --

# -- Log --------------------------------------------------------------------------

get_event_loop().run_until_complete(core.logger.save("Loaded email module successfully.", core.logger.DEBUG))

# -------------------------------------------------------------------------- Log --
