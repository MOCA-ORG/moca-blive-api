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

from smtplib import SMTP_SSL, SMTP, SMTPException
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import List, Union, Optional
from aiosmtplib import send, SMTPException as AsyncSMTPException
from .. import core
from asyncio import get_event_loop
from moca_log import MocaLog

# -------------------------------------------------------------------------- Imports --

# -- Private Functions --------------------------------------------------------------------------


def _create_client(user_name: str,
                   password: str) -> Optional[Union[SMTP, SMTP_SSL]]:
    """
    create a SMTP client.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :return: SMTP or SMTP_SSL instance. If some error occurred, return None.
    """
    try:
        if core.config.get('smtp_use_ssl', bool, True):
            client = SMTP_SSL(core.config.get('smtp_host', str, ''),
                              core.config.get('smtp_port', int, 465))
        else:
            client = SMTP(core.config.get('smtp_host', str, ''),
                          core.config.get('smtp_port', int, 25))
        client.login(user_name, password)
        get_event_loop().run_until_complete(
            core.logger.save('Connected to smtp server.', core.logger.DEBUG)
        )
        return client
    except SMTPException as error:
        get_event_loop().run_until_complete(
            core.logger.save(f"Can't connect to smtp server. <SMTPException: {error}>", core.logger.WARNING, True)
        )
        return None


# -------------------------------------------------------------------------- Private Functions --

# -- Send Email --------------------------------------------------------------------------


def send_mail(user_name: str,
              password: str,
              from_address: str,
              to_address: List[str],
              body: str,
              title: str,
              mail_type: str = 'plain') -> bool:
    """
    Send a mail.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :param from_address: the from address.
    :param to_address: the to address.
    :param body: the body of the email.
    :param title: the title of the email.
    :param mail_type: the type of the email, plain or html.
    :return: status
    """
    client = _create_client(user_name, password)
    if client is None:
        get_event_loop().run_until_complete(
            core.logger.save("Send mail failed, Can't connect to smtp server.", core.logger.WARNING)
        )
        return False
    msg = MIMEText(body, mail_type, 'utf-8')
    msg['Subject'] = title
    msg['From'] = from_address
    msg['To'] = ','.join(to_address)
    msg['Date'] = formatdate()
    try:
        client.sendmail(from_address, to_address, msg.as_string())
        get_event_loop().run_until_complete(
            core.logger.save(f"Send mail success. <Title: {title}, To: {','.join(to_address)}>", core.logger.DEBUG)
        )
        return True
    except SMTPException as error:
        get_event_loop().run_until_complete(
            core.logger.save(f'Send mail failed. <SMTPException: {error}>', core.logger.WARNING, True)
        )
        return False


async def send_aio_mail(user_name: str,
                        password: str,
                        from_address: str,
                        to_address: List[str],
                        body: str,
                        title: str,
                        logger: MocaLog,
                        mail_type: str = 'plain') -> bool:
    """
    Send a mail.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :param from_address: the from address.
    :param to_address: the to address.
    :param body: the body of the email.
    :param title: the title of the email.
    :param logger: a MocaLog instance.
    :param mail_type: the type of the email, plain or html.
    :return: status
    """
    msg = MIMEText(body, mail_type, 'utf-8')
    msg['Subject'] = title
    msg['From'] = from_address
    msg['To'] = ','.join(to_address)
    msg['Date'] = formatdate()
    try:
        await send(message=msg.as_string(),
                   sender=from_address,
                   recipients=to_address,
                   hostname=core.config.get('smtp_host', str, ''),
                   port=core.config.get('smtp_port', int, 465),
                   username=user_name,
                   password=password,
                   use_tls=core.config.get('smtp_use_ssl', bool, True))
        await logger.save(f"Send mail success. <Title: {title}, To: {','.join(to_address)}>",
                          logger.DEBUG)
        return True
    except AsyncSMTPException as error:
        await logger.save(f'Send mail failed. <SMTPException: {error}>', logger.ERROR, True)
        return False


def send_notification_mail(message: str) -> bool:
    return send_mail(core.config.get('smtp_notification_user', str, ''),
                     core.config.get('smtp_notification_pass', str, ''),
                     core.config.get('smtp_notification_from_address', str, ''),
                     core.config.get('smtp_notification_to_address', list, ['']),
                     message,
                     '[BliveCommentAPI] System Notification',
                     'html')


async def send_aio_notification_mail(message: str, logger: MocaLog) -> bool:
    return await send_aio_mail(core.config.get('smtp_notification_user', str, ''),
                               core.config.get('smtp_notification_pass', str, ''),
                               core.config.get('smtp_notification_from_address', str, ''),
                               core.config.get('smtp_notification_to_address', list, ['']),
                               message,
                               '[BliveCommentAPI] System Notification',
                               logger,
                               'html')

# -------------------------------------------------------------------------- Send Email --
