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
Copyright (c) 2020.5.28 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaSystem/LICENSE/
"""


# -- Imports --------------------------------------------------------------------------

from typing import *
from smtplib import SMTP_SSL, SMTP
from email.mime.text import MIMEText
from email.utils import formatdate
from aiosmtplib import send
from .moca_base_class import MocaNamedInstance, MocaClassCache

# -------------------------------------------------------------------------- Imports --

# -- Private Functions --------------------------------------------------------------------------


def create_client(user_name: str, password: str, ssl: bool, host: str, port: int) -> Union[SMTP, SMTP_SSL]:
    """
    create a SMTP client.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :param ssl: connect use ssl.
    :param host: the host of the smtp server.
    :param port: the port of the smtp server.
    :return: SMTP or SMTP_SSL instance. If some error occurred, return None.
    """
    client: Union[SMTP, SMTP_SSL]
    if ssl:
        client = SMTP_SSL(host, port)
    else:
        client = SMTP(host, port)
    client.login(user_name, password)
    return client

# -------------------------------------------------------------------------- Private Functions --

# -- Mail --------------------------------------------------------------------------


def send_mail(user_name: str,
              password: str,
              ssl: bool,
              host: str,
              port: int,
              from_address: str,
              to_address: List[str],
              body: str,
              title: str,
              mail_type: str = 'plain') -> None:
    """
    Send a mail.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :param ssl: connect use ssl.
    :param host: the host of the smtp server.
    :param port: the port of the smtp server.
    :param from_address: the from address.
    :param to_address: the to address.
    :param body: the body of the email.
    :param title: the title of the email.
    :param mail_type: the type of the email, plain or html.
    Raise: smtplib.SMTPException
    """
    client = create_client(user_name, password, ssl, host, port)
    msg = MIMEText(body, mail_type, 'utf-8')
    msg['Subject'] = title
    msg['From'] = from_address
    msg['To'] = ','.join(to_address)
    msg['Date'] = formatdate()
    client.sendmail(from_address, to_address, msg.as_string())


async def send_aio_mail(user_name: str,
                        password: str,
                        ssl: bool,
                        host: str,
                        port: int,
                        from_address: str,
                        to_address: List[str],
                        body: str,
                        title: str,
                        mail_type: str = 'plain') -> None:
    """
    Send a mail.
    :param user_name: the user name of the smtp server.
    :param password: the password of the smtp server.
    :param ssl: connect use ssl.
    :param host: the host of the smtp server.
    :param port: the port of the smtp server.
    :param from_address: the from address.
    :param to_address: the to address.
    :param body: the body of the email.
    :param title: the title of the email.
    :param mail_type: the type of the email, plain or html.
    :return: status
    Raise:
        aiosmtplib.SMTPException
    """
    msg = MIMEText(body, mail_type, 'utf-8')
    msg['Subject'] = title
    msg['From'] = from_address
    msg['To'] = ','.join(to_address)
    msg['Date'] = formatdate()
    await send(message=msg.as_string(),
               sender=from_address,
               recipients=to_address,
               hostname=host,
               port=port,
               username=user_name,
               password=password,
               use_tls=ssl)


class MocaMail(MocaNamedInstance, MocaClassCache):
    """
    A simple mail class.

    Attributes
    ----------
    self._user_name: str
        the user name of the smtp server.
    self._password: str
        the password of the smtp server.
    self._from: str
        the from address.
    self._ssl: bool
        connect use ssl.
    self._host: str
        the host of the smtp server.
    self._port: int
        the port of the smtp server.
    """

    def __init__(self, user_name: str, password: str, from_address: str, ssl: bool, host: str, port: int):
        """
        :param user_name: the user name of the smtp server.
        :param password: the password of the smtp server.
        :param from_address: the from address.
        :param ssl: connect use ssl.
        :param host: the host of the smtp server.
        :param port: the port of the smtp server.
        Raise: smtplib.SMTPException
        """
        MocaNamedInstance.__init__(self)
        MocaClassCache.__init__(self)
        self._user_name: str = user_name
        self._password: str = password
        self._from: str = from_address
        self._ssl: bool = ssl
        self._host: str = host
        self._port: int = port

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def ssl(self) -> bool:
        return self._ssl

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    async def send_aio_mail(self,
                            to_address: List[str],
                            body: str,
                            title: str,
                            mail_type: str = 'plain') -> None:
        """
        Send a mail.
        :param to_address: the to address.
        :param body: the body of the email.
        :param title: the title of the email.
        :param mail_type: the type of the email, plain or html.
        :return: status
        Raise:
            aiosmtplib.SMTPException
        """
        msg = MIMEText(body, mail_type, 'utf-8')
        msg['Subject'] = title
        msg['From'] = self._from
        msg['To'] = ','.join(to_address)
        msg['Date'] = formatdate()
        await send(message=msg.as_string(),
                   sender=self._from,
                   recipients=to_address,
                   hostname=self._host,
                   port=self._port,
                   username=self._user_name,
                   password=self._password,
                   use_tls=self._ssl)

    def send_mail(self,
                  to_address: List[str],
                  body: str,
                  title: str,
                  mail_type: str = 'plain') -> None:
        """
        Send a mail.
        :param to_address: the to address.
        :param body: the body of the email.
        :param title: the title of the email.
        :param mail_type: the type of the email, plain or html.
        Raise: smtplib.SMTPException
        """
        client = create_client(self._user_name, self._password, self._ssl, self._host, self._port)
        msg = MIMEText(body, mail_type, 'utf-8')
        msg['Subject'] = title
        msg['From'] = self._from
        msg['To'] = ','.join(to_address)
        msg['Date'] = formatdate()
        client.sendmail(self._from, to_address, msg.as_string())

# -------------------------------------------------------------------------- Mail --
