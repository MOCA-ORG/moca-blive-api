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

from aiosmtplib import SMTPException, send
from email.mime.text import MIMEText
from email.utils import formatdate
from .save_log import save_log
from .core import moca_config

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('smtp_server_host', str, '')
moca_config.get('smtp_server_port', int, 25)
moca_config.get('smtp_server_user', str, '')
moca_config.get('smtp_server_pass', str, '')
moca_config.get('smtp_from_address', str, '')
moca_config.get('smtp_use_ssl', bool, True)
moca_config.get('smtp_to_address', list, [])
moca_config.get('smtp_mail_title', str, 'BliveCommentAPI')
moca_config.get('send_mail_if_found_unknown_gift_name', bool, False)
moca_config.get('send_mail_if_start_listen', bool, False)
moca_config.get('send_mail_if_stop_listen', bool, False)

# -------------------------------------------------------------------------- Init --

# -- Send Mail --------------------------------------------------------------------------


async def send_mail(message: str) -> bool:
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = moca_config.get('smtp_mail_title', str, 'BliveCommentAPI')
    msg['From'] = moca_config.get('smtp_from_address', str, '')
    msg['To'] = ','.join(moca_config.get('smtp_to_address', list, []))
    msg['Date'] = formatdate()
    try:
        await send(message=msg.as_string(),
                   sender=moca_config.get('smtp_from_address', str, ''),
                   recipients=moca_config.get('smtp_to_address', list, []),
                   hostname=moca_config.get('smtp_server_host', str, ''),
                   port=moca_config.get('smtp_server_port', int, 25),
                   username=moca_config.get('smtp_server_user', str, ''),
                   password=moca_config.get('smtp_server_pass', str, ''),
                   use_tls=moca_config.get('smtp_use_ssl', bool, True))
        return True
    except SMTPException as error:
        save_log('邮件发送失败。<SMTPException: %s>' % error)
        return False


async def send_unknown_gift_mail(message: str) -> bool:
    if moca_config.get('send_mail_if_found_unknown_gift_name', bool, False):
        await send_mail(message)
    else:
        return True


async def send_start_listen_mail(message: str) -> bool:
    if moca_config.get('send_mail_if_start_listen', bool, False):
        await send_mail(message)
    else:
        return True


async def send_stop_listen_mail(message: str) -> bool:
    if moca_config.get('send_mail_if_stop_listen', bool, False):
        await send_mail(message)
    else:
        return True

# -------------------------------------------------------------------------- Send Mail --
