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

from .moca_redis import MocaRedis
from .moca_mysql import MocaMysql
from .moca_base_class import MocaNamedInstance, MocaClassCache
from .moca_mail import MocaMail
from .moca_sms import MocaTwilioSMS
from .moca_utils import *
from .moca_variables import tz
from .moca_utils import moca_dumps as dumps, moca_loads as loads
from uuid import uuid4
from hashlib import sha1, sha256
from secrets import compare_digest
from datetime import datetime
from pathlib import Path
from pymysql.err import IntegrityError
from aiosmtplib import SMTPException
from aiofiles import open
from typing import *
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pymysql.err import DataError
from twilio.base.exceptions import TwilioException
from gzip import compress, decompress
from ujson import dumps as json_dumps, loads as json_loads

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

DUMMY_DATA = [
    {'name': 'ルルーシュ・ランペルージ', 'pass': 'Lelouch Lamperouge', 'id': 'Lelouch Lamperouge', 'email': 'lelouch@el.el'},
    {'name': '枢木 スザク', 'pass': 'Suzaku Kururugi', 'id': 'Suzaku Kururugi', 'email': 'kururugi@el.el'},
    {'name': 'c.c', 'pass': 'cccccccccc', 'id': 'cccccccccc', 'email': 'cc@el.el'},
    {'name': '紅月カレン', 'pass': 'Kallen Kouzuki', 'id': 'Kallen Kouzuki', 'email': 'kouzuki@el.el'},
    {'name': 'ナナリー・ランペルージ', 'pass': 'Nunnally Lamperouge', 'id': 'Nunnally Lamperouge', 'email': 'nunnally@el.el'},
    {'name': 'ロロ・ランペルージ', 'pass': 'Rolo Lamperouge', 'id': 'Rolo Lamperouge', 'email': 'roro@el.el'},
    {'name': 'シャーリー・フェネット', 'pass': 'Shirley Fenette', 'id': 'Shirley Fenette', 'email': 'shirley@el.el'},
    {'name': 'ミレイ・アッシュフォード', 'pass': 'Milly Ashford', 'id': 'Milly Ashford', 'email': 'milly@el.el'},
    {'name': 'リヴァル・カルデモンド', 'pass': 'Rivalz Cardemonde', 'id': 'Rivalz Cardemonde', 'email': 'rivalz@el.el'},
    {'name': 'ニーナ・アインシュタイン', 'pass': 'Nina Einstein', 'id': 'Nina Einstein', 'email': 'nina@el.el'},
    {'name': 'アーサー', 'pass': 'Arthur', 'id': 'Arthur', 'email': 'arthur@el.el'},
    {'name': '扇要', 'pass': 'Kaname Ohgi', 'id': 'Kaname Ohgi', 'email': 'ohgi@el.el'},
    {'name': '玉城真一郎', 'pass': 'Shinichirō Tamaki', 'id': 'Shinichirō Tamaki', 'email': 'tamaki@el.el'},
    {'name': '藤堂鏡志朗', 'pass': 'Kyoshiro Tohdoh', 'id': 'Kyoshiro Tohdoh', 'email': 'tohdoh@el.el'},
    {'name': 'ディートハルト・リート', 'pass': 'Diethard Ried', 'id': 'Diethard Ried', 'email': 'diethard@el.el'},
    {'name': 'ラクシャータ・チャウラー', 'pass': 'Rakshata Chawla', 'id': 'Rakshata Chawla', 'email': 'rakshata@el.el'},
    {'name': '皇神楽耶', 'pass': 'Kaguya Sumeragi', 'id': 'Kaguya Sumeragi', 'email': 'kaguya@el.el'},
    {'name': '桐原泰三', 'pass': 'Taizō Kirihara', 'id': 'Taizō Kirihara', 'email': 'kirihara@el.el'},
    {'name': '篠崎咲世子', 'pass': 'Sayoko Shinozaki', 'id': 'Sayoko Shinozaki', 'email': 'sayoko@el.el'},
    {'name': 'シャルル・ジ・ブリタニア', 'pass': 'Charles zi Britannia', 'id': 'Charles zi Britannia', 'email': 'charles@el.el'},
    {'name': 'コーネリア・リ・ブリタニア', 'pass': 'Cornelia li Britannia', 'id': 'Cornelia li Britannia', 'email': 'cornelia@el.el'},
    {'name': 'ユーフェミア・リ・ブリタニア', 'pass': 'Euphemia li Britannia', 'id': 'Euphemia li Britannia', 'email': 'euphemia@el.el'},
    {'name': 'マリアンヌ・ヴィ・ブリタニア', 'pass': 'Marianne vi Britannia', 'id': 'Marianne vi Britannia', 'email': 'marianne@el.el'},
    {'name': 'アーニャ・アールストレイム', 'pass': 'Anya Alstreim', 'id': 'Anya Alstreim', 'email': 'anya@el.el'},
    {'name': 'ジェレミア・ゴットバルト', 'pass': 'Orange', 'id': 'Orange', 'email': 'orange@el.el'},
    {'name': 'ヴィレッタ・ヌゥ', 'pass': 'Villetta Nu', 'id': 'Villetta Nu', 'email': 'villetta@el.el'},
    {'name': 'ギルバート・G・P・ギルフォード', 'pass': 'Gilbert G.P. Guilford', 'id': 'Gilbert G.P. Guilford', 'email': 'gilbert@el.el'},
    {'name': 'ロイド・アスプルンド', 'pass': 'Lloyd Asplund', 'id': 'Lloyd Asplund', 'email': 'lloyd@el.el'},
    {'name': '黎星刻', 'pass': 'Li Xingke', 'id': 'Li Xingke', 'email': 'xingke@el.el'},
    {'name': '蒋麗華', 'pass': 'Jiang Lihua', 'id': 'Jiang Lihua', 'email': 'tianzi@el.el'},
    {'name': '周香凛', 'pass': 'Zhou Xiangling', 'id': 'Zhou Xiangling', 'email': 'zhou@el.el'},
    {'name': 'マオ', 'pass': 'MaoMaoMao', 'id': 'Mao', 'email': 'mao@el.el'},
    {'name': 'V.V', 'pass': 'vvvvvvvvvv', 'id': 'vvvvvvvvvv', 'email': 'vv@el.el'},
    {'name': 'シャムナ', 'pass': 'Shamna', 'id': 'Shamna', 'email': 'shamna@el.el'},
    {'name': 'シャリオ', 'pass': 'Shalio', 'id': 'Shalio', 'email': 'shalio@el.el'},
]

# -------------------------------------------------------------------------- Variables --

# -- MocaUsers --------------------------------------------------------------------------


class MocaUsers(MocaNamedInstance, MocaClassCache):
    """
    User management system.

    Attributes
    ----------
    _mysql: MocaMysql = mysql
        a instance of MocaMysql.
    _redis: MocaRedis = redis
        a instance of MocaRedis.
    _mail: MocaMail = mail
        a instance of MocaMail.
    _sms: MocaTwilioSMS = sms
        a instance of MocaTwilioSMS.
    _users_dir: Path
        a directory to save user data.
    _username: Tuple[int, int, bool]
        username_max_length, username_min_length, username_only_ascii
    _userpass: Tuple[int, int, bool, bool, bool, bool]
        userpass_max_length, userpass_min_length, userpass_must_contain_alphabet,
        userpass_must_contain_digits, userpass_must_contain_symbols, userpass_only_ascii,
        userpass_must_contain_upper, userpass_must_contain_lower
    _user_id: Tuple[int, int]
        userid_max_length, userid_min_length
    _email_is_required: bool
        all user must have an email address.
    access_token_lifetime: int
        the lifetime(s) of the access token.
    email_token_lifetime: int
        the lifetime(s) of the email verification code.
    _save_raw_password: bool
        save the raw password. don't use hash.
    User Status
    ----------- ¥
    C : correct, this account can login to system.
    L : locked, this account can not login to system, locked by system.
    S : stop, this account can not login to system, locked by user.
    E : el, this is a system account.
    P: phone, this account need sms verification.
    Permission
    ----------
    -RT-: do anything.
    -MU-: manage user account.
    """

    # storage0, 1 - public storage
    # storage2, 3, 4, 5, 6, 7 - private storage
    _USER_TABLE = """
    create table if not exists moca_users(
        id varchar(%s) primary key,
        status varchar(1),
        name varchar(%s),
        email varchar(255),
        email_verified varchar(1),
        password varchar(%s),
        phone varchar(32),
        profile varchar(2048) default null,
        storage0 blob default null,
        storage1 blob default null,
        storage2 blob default null,
        storage3 blob default null,
        storage4 blob default null,
        storage5 blob default null,
        storage6 mediumblob default null,
        storage7 mediumblob default null,
        permission varchar(64) default null,
        created_at varchar(32)
    );
    """

    _USER_LOGIN_LOG_TABLE = """
    create table if not exists moca_login_log(
        id varchar(%s),
        ip varchar(64),
        info varchar(64),
        status varchar(1),
        time datetime
    );
    """

    _USER_STORAGE = """
    create table if not exists moca_user_storage(
        content_id bigint auto_increment primary key,
        user_id varchar(%s),
        data_key varchar(64),
        storage mediumblob default null,
        created_at datetime not null
    );
    """

    _USER_MESSAGES = """
    create table if not exists moca_user_messages(
        id bigint auto_increment primary key,
        from_ varchar(%s) not null,
        to_ varchar(%s) not null,
        message varchar(8192) not null,
        time datetime not null
    );
    """

    _SAVE_USER_DATA = """
    update moca_users set storage%s = %s where id = %s;
    """

    _GET_USER_DATA = """
    select storage%s from moca_users where id = %s;
    """

    _SEND_MESSAGE = """
    insert into moca_user_messages(from_, to_, message, time)
    values(%s,%s,%s,now())
    """

    _GET_MESSAGES = """
    select id, from_, message, time from moca_user_messages where to_ = %s order by time limit %s, %s;
    """

    _CREATE_USER = """
    insert into moca_users(id, status, name, email, email_verified, password, phone, permission, created_at)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """

    _GET_EMAIL = """
    select email, email_verified from moca_users where id = %s
    """

    _VERIFY_EMAIL = """
    update moca_users set email_verified = %s where id = %s;
    """

    _GET_USER_INFO = """
    select * from moca_users where id = %s;
    """

    _GET_LOGIN_INFO = """
    select id, status, name, email, email_verified, password, phone from moca_users where id = %s;
    """

    _CHECK_USER = """
    select id from moca_users where id = %s;
    """

    _SAVE_LOGIN_LOG = """
    insert into moca_login_log(id, ip, info, status, time)
    values(%s,%s,%s,%s,now());
    """

    _SEARCH_USERS_BY_NAME = """
    select id, name, profile, storage0, storage1, created_at from moca_users
    where name like %s and (status = 'C' or status = 'P');
    """

    _SEARCH_USER_BY_ID = """
    select id, name, profile, storage0, storage1, created_at from moca_users
    where id = %s and (status = 'C' or status = 'P');
    """

    _SAVE_PROFILE = """
    update moca_users set profile = %s where id = %s;
    """

    _GET_PROFILE = """
    select profile from moca_users where id = %s;
    """

    _UPDATE_PHONE = """
    update moca_users set phone = %s where id = %s;
    """

    _GET_PHONE = """
    select phone from moca_users where id = %s;
    """

    _CHECK_PASSWORD = """
    select id from moca_users where id = %s and password = %s;
    """

    _UPDATE_STATUS = """
    update moca_users set status = %s where id = %s;
    """

    _UPDATE_EMAIL_STATUS = """
    update moca_users set email_verified = %s where id = %s;
    """

    _GET_PERMISSION = """
    select permission from moca_users where id = %s and password = %s and status = 'E';
    """

    _DROP_DB = """
    drop table if exists moca_users, moca_user_storage, moca_login_log;
    """

    _GET_LOGIN_LOG = """
    select * from moca_login_log where id = %s order by time;
    """

    _ADD_EMAIL = """
    update moca_users set email = %s where id = %s;
    """

    _IS_SYSTEM_ACCOUNT = """
    select id from moca_users where id = %s and status = 'E';
    """

    _GET_PASS = """
    select password from moca_users where id = %s;
    """

    _UPDATE_PASS = """
    update moca_users set password = %s where id = %s;
    """

    _GET_USER_NUMBER = """
    select count(*) from moca_users where status != 'E';
    """

    _GET_LOCKED_USER_NUMBER = """
    select count(*) from moca_users where status = 'L' or status = 'S';
    """

    _GET_USERS_LIST = """
    select id, status, name, email, email_verified, phone, created_at from moca_users order by created_at limit %s, %s;
    """

    _INSERT_DATA_TO_STORAGE = """
    insert into moca_user_storage(user_id, data_key, storage, created_at)
    values(%s,%s,%s,now());
    """

    _SELECT_DATA_FROM_STORAGE = """
    select content_id, storage, created_at from moca_user_storage where user_id = %s and data_key = %s;
    """

    _DELETE_DATA_FROM_STORAGE_BY_ID = """
    delete from moca_user_storage where user_id = %s and content_id = %s;
    """

    _DELETE_DATA_FROM_STORAGE_BY_KEY = """
    delete from moca_user_storage where user_id = %s and data_key = %s;
    """

    _UPDATE_DATA_IN_STORAGE = """
    update moca_user_storage set storage = %s where user_id = %s and content_id = %s;
    """

    VERIFICATION_MAIL_BODY = "Your verification code is <%s> \n\r Please enter your verification code in 7 days."
    VERIFICATION_MAIL_TITLE = "Please check your verification code."

    FORGOT_PASS_BODY = "Your verification code is <%s> \n\r Please enter your verification code in 10 minutes."
    FORGOT_PASS_TITLE = "Reset your password."

    def __init__(self, mysql: MocaMysql, redis: MocaRedis, mail: MocaMail, sms: MocaTwilioSMS,
                 users_dir: Union[Path, str], username_max_length: int = 32, username_min_length: int = 1,
                 username_only_ascii: bool = False, userpass_max_length: int = 32, userpass_min_length: int = 8,
                 userpass_must_contain_alphabet: bool = False, userpass_must_contain_digits: bool = False,
                 userpass_must_contain_upper: bool = False, userpass_must_contain_lower: bool = False,
                 userpass_must_contain_symbols: bool = False, userpass_only_ascii: bool = True,
                 userid_max_length: int = 32, userid_min_length: int = 1, email_is_required: bool = False,
                 save_raw_password: bool = False):
        """

        :param mysql: a instance of MocaMysql.
        :param redis: a instance of MocaRedis.
        :param mail: a instance of MocaMail.
        :param sms: a instance of MocaTwilioSMS.
        :param users_dir: a directory to save user data.
        :param username_max_length: the maximum length of the username.
        :param username_min_length: the minimum length of the username..
        :param username_only_ascii: only allow ascii characters in username.
        :param userpass_max_length: the maximum length of the user password.
        :param userpass_min_length: the minimum length of the user password.
        :param userpass_must_contain_alphabet: password must contains alphabet.
        :param userpass_must_contain_digits: password must contains digits.
        :param userpass_must_contain_upper: password must contains upper case
        :param userpass_must_contain_lower: password must contains lower case
        :param userpass_must_contain_symbols: password must contains symbols.
        :param userpass_only_ascii: only allow ascii characters in password.
        :param userid_max_length: the maximum length of the user identifier.
        :param userid_min_length: the minimum length of the user identifier.
        :param email_is_required: all user must have an email address.
        :param save_raw_password: save the raw password. don't use hash.
        """
        MocaNamedInstance.__init__(self)
        MocaClassCache.__init__(self)
        self._mysql: MocaMysql = mysql
        self._redis: MocaRedis = redis
        self._mail: MocaMail = mail
        self._sms: MocaTwilioSMS = sms
        self._users_dir: Path
        if isinstance(users_dir, str):
            self._users_dir = Path(users_dir)
        else:
            self._users_dir = users_dir
        self._username: Tuple[int, int, bool] = (
            username_max_length, username_min_length, username_only_ascii
        )
        self._userpass: Tuple[int, int, bool, bool, bool, bool, bool, bool] = (
            userpass_max_length, userpass_min_length, userpass_must_contain_alphabet,
            userpass_must_contain_digits, userpass_must_contain_symbols, userpass_only_ascii,
            userpass_must_contain_upper, userpass_must_contain_lower,
        )
        self._user_id: Tuple[int, int] = (userid_max_length, userid_min_length)
        self._email_is_required: bool = email_is_required
        self.access_token_lifetime: int = 60 * 60 * 24 * 30 * 3  # 3 month
        self.email_token_lifetime: int = 60 * 60 * 24 * 7  # 7 days
        self._save_raw_password: bool = save_raw_password
        self._users_dir.joinpath('shared_files').mkdir(parents=True, exist_ok=True)

    async def init_db(self) -> None:
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(
                    MocaUsers._USER_TABLE,
                    (self._user_id[0], self._username[0], self._userpass[0])
                )
                await cursor.execute(MocaUsers._USER_LOGIN_LOG_TABLE, (self._user_id[0],))
                await cursor.execute(MocaUsers._USER_STORAGE, (self._user_id[0],))
                await cursor.execute(MocaUsers._USER_MESSAGES, (self._user_id[0], self._user_id[0]))
                await con.commit()
        await self._init_system_account()

    async def _init_system_account(self) -> None:
        await self.create_user('Administrator', 'moca', 'moca.administrator', '', True, '-RT-')
        await self.create_user('UserAdmin', 'moca', 'moca.user-admin', '', True, '-MU-')
        await self.create_user('PublicUser', 'moca', 'moca.public', '', True, '')
        await self.create_user('SupportUser', 'moca', 'moca.support', '', True, '')
        await self.create_user('DebugAccountA', 'moca', 'moca.debug-a', '', True, '')
        await self.create_user('DebugAccountB', 'moca', 'moca.debug-b', '', True, '')
        await self.create_user('DebugAccountC', 'moca-moca-moca', 'moca.debug-c', '', False, '')
        await self.create_user('DebugAccountD', 'moca-moca-moca', 'moca.debug-d', '', False, '')

    async def insert_dummy_data(self) -> None:
        for item in DUMMY_DATA:
            await self.create_user(item['name'], item['pass'], item['id'], item['email'])

    def _check_userid_format(self, userid: str) -> Tuple[int, str]:
        if not isinstance(userid, str):
            return 60, 'user id must be a string.'
        elif not (self._user_id[1] <= len(userid) <= self._user_id[0]):
            return 61, 'user id length error.'
        elif not userid.isascii():
            return 63, 'user is must only contains ascii characters.'
        else:
            return 0, 'correct.'

    def _check_username_format(self, username: str) -> Tuple[int, str]:
        if not isinstance(username, str):
            return 40, 'user name must be a string.'
        elif not (self._username[1] <= len(username) <= self._username[0]):
            return 41, 'user name length error.'
        elif self._username[2] and (not username.isascii()):
            return 42, 'only ASCII characters allowed in username.'
        else:
            return 0, 'correct.'

    def _check_password_format(self, password: str) -> Tuple[int, str]:
        if not isinstance(password, str):
            return 50, 'password must be a string.'
        elif not (self._userpass[1] <= len(password) <= self._userpass[0]):
            return 51, 'password length error.'
        elif self._userpass[2] and (not contains_alpha(password)):  # must contains alphabet.
            return 52, 'password must contains a alphabet.'
        elif self._userpass[3] and (not contains_digit(password)):  # must contains digits.
            return 53, 'password must contains a number.'
        elif self._userpass[4] and (not contains_symbol(password)):  # must contains symbol.
            return 54, 'password must contains a symbol.'
        elif self._userpass[5] and (not password.isascii()):  # must only contains ascii.
            return 55, 'password must only contains ascii characters.'
        elif self._userpass[6] and (not contains_upper(password)):  # must contains upper case characters.
            return 56, 'password must contains upper case characters.'
        elif self._userpass[7] and (not contains_lower(password)):  # must contains lower case characters.
            return 57, 'password must contain lower case characters.'
        else:
            return 0, 'correct.'

    @staticmethod
    def _check_email_format(email: str) -> Tuple[int, str]:
        if not isinstance(email, str):
            return 70, 'email must be a string.'
        elif len(email) > 255:
            return 71, 'email is too long.'
        elif not check_email_format(email):
            return 73, 'email format error.'
        else:
            return 0, 'correct.'

    async def create_user(self, username: str, password: str,
                          userid: str, email: Optional[str] = None,
                          is_system: bool = False, permission: str = '') -> Tuple[int, str]:
        """"
        Return: status_code, response_message.
        Status Code
        -----------
        0: create user successfully.
        1: can't use this user id.
        40: user name must be a string.
        41: user name length error.
        42: only ASCII characters allowed in username.
        50: password must be a string.
        51: password length error.
        52: password must contains a alphabet.
        53: password must contains a number.
        54: password must contains a symbol.
        55: password must only contains ascii characters.
        56: password must contains upper case characters.
        57: password must contain lower case characters.
        60: userid must be a string.
        61: user id length error.
        62: user id already exists.
        63: user is must only contains ascii characters.
        70: email must be a string.
        71: email is too long.
        72: email is required.
        73: email format error.
        """
        if not is_system:
            res = self._check_username_format(username)
            if res[0] != 0:
                return res
            res = self._check_userid_format(userid)
            if res[0] != 0:
                return res
            if (not is_system) and (userid.startswith('el.') or userid.startswith('moca.')):
                return 1, "can't use this user id."
            res = self._check_password_format(password)
            if res[0] != 0:
                return res
            if email is None and self._email_is_required:
                return 72, 'email is required.'
            if email is not None:
                res = self._check_email_format(email)
            if res[0] != 0:
                return res
        try:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(
                        MocaUsers._CREATE_USER,
                        (userid, 'C' if not is_system else 'E', username, email if email is not None else '', 'F',
                         password if self._save_raw_password else sha256(password.encode()).hexdigest(),
                         '', permission, str(datetime.now(tz)))
                    )
                    await con.commit()
            return 0, 'create user successfully.'
        except IntegrityError:
            return 62, 'user id already exists.'

    async def check_userid(self, userid: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: unknown user.
        1: user id already exists.
        60: user id must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._CHECK_USER, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return 0, 'unknown user.'
                else:
                    return 1, 'user id already exists.'

    async def _verify_email(self, userid: str, key: str):
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        log = await self._redis.get(key + userid)
        if log is not None:
            return 3, 'too quickly.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_EMAIL, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return 1, 'unknown user.'
                elif data[0][1] == 'T':
                    return 2, 'already verified.'
        return -1, data

    async def send_email_verify_message(self, userid: str) -> Tuple[int, str]:
        """
        Send a verification code to the email address.
        Return: status_code, response_message.
        Status Code
        -----------
        0: send verification code successfully.
        1: unknown user.
        2: already verified.
        3: too quickly.
        4: can't send verification code.
        5: this account do not have a email address.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self._verify_email(userid, 'moca-user-send-email-verify-')
        if res[0] != -1:
            return res
        if res[1][0][0] == '' or res[1][0][0] is None:
            return 5, 'this account do not have a email address.'
        await self._redis.save('moca-user-send-email-verify-' + userid, 'send', 60)  # can send once per 60 seconds
        try:
            verification_code = uuid4().hex[:6]
            await self._redis.save('moca-user-email-verification-code-' + userid,
                                   verification_code,
                                   self.email_token_lifetime)
            body = MocaUsers.VERIFICATION_MAIL_BODY % verification_code
            await self._mail.send_aio_mail([res[1][0][0]], body, MocaUsers.VERIFICATION_MAIL_TITLE, 'plain')
            return 0, 'send verification code successfully.'
        except SMTPException:
            return 4, "can't send verification code."

    async def add_email_address(self, userid: str, email: str, access_token: str) -> Tuple[int, str]:
        """
        Send a verification code to the email address.
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        70: email must be a string.
        71: email is too long.
        73: email format error.
        """
        res = self._check_email_format(email)
        if res[0] != 0:
            return res
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._ADD_EMAIL, (email, userid))
                await cursor.execute(MocaUsers._UPDATE_EMAIL_STATUS, ())
                await con.commit()
        return 0, 'success.'

    async def verify_email(self, userid: str, token: str) -> Tuple[int, str]:
        """
        Verify email address by token.
        Return: status_code, response_message.
        Status Code
        -----------
        0: verification successfully.
        1: unknown user.
        2: already verified.
        3: token error.
        4, token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self._verify_email(userid, 'moca-user-email-verify-')
        if res[0] != -1:
            return res
        if (not isinstance(token, str)) or (len(token) != 6):
            return 4, 'token format error.'
        await self._redis.save('moca-user-email-verify-' + userid, 'verify', 5)  # can verify once per 5 seconds
        if compare_digest(token, str(await self._redis.get('moca-user-email-verification-code-' + userid))):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._VERIFY_EMAIL, ('T', userid))
                    await con.commit()
                    return 0, 'verification successfully.'
        else:
            return 3, 'token error.'

    async def _is_system_account(self, userid: str) -> bool:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return False
        cache = await self._redis.get('moca-is-system-account-' + userid)
        if cache is not None:
            return True
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._IS_SYSTEM_ACCOUNT, (userid,))
                data = await cursor.fetchall()
                if len(data) > 0:
                    await self._redis.save('moca-is-system-account-' + userid, 'T')
                    return True
                else:
                    return False

    async def _get_password(self, userid: str) -> str:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return ''
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_PASS, (userid,))
                data = await cursor.fetchall()
                if len(data) > 0:
                    return data[0][0]
                else:
                    return ''

    async def _get_access_token(self, userid: str) -> str:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return 'None'
        cache = await self._redis.get('moca-user-access-token-' + userid)
        if cache is None:
            if await self._is_system_account(userid):
                token = await self._get_password(userid)
                await self._redis.save('moca-user-access-token-' + userid, token)
            else:
                token = uuid4().hex
                await self._redis.save('moca-user-access-token-' + userid, token, self.access_token_lifetime)
        else:
            token = cache
        return token

    async def check_access_token(self, userid: str, token: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: correct.
        1: incorrect token.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if (not isinstance(token, str)) or ((len(token) != 32) and (not await self._is_system_account(userid))):
            return 3, 'token format error.'
        if compare_digest(str(await self._get_access_token(userid)), token):
            return 0, 'correct.'
        else:
            return 1, 'incorrect token.'

    async def login(self, userid: str, password: str, ip: str = 'unknown') -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        -2: ip format error.
        -1: verification code send to your phone.
        0: <access token>.
        1: unknown user.
        2: this user account was locked by system.
        3: this user account was locked by user.
        4: system account can not login.
        5: unknown user status.
        6: please verify your email address. before login.
        7: incorrect password.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        50: password must be a string.
        51: password length error.
        52: password must contains a alphabet.
        53: password must contains a number.
        54: password must contains a symbol.
        55: password must only contains ascii characters.
        56: password must contains upper case characters.
        57: password must contain lower case characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        res = self._check_password_format(password)
        if res[0] != 0:
            return res
        if (not isinstance(ip, str)) or (len(ip) > 64):
            return -2, 'ip format error.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_LOGIN_INFO, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return 1, 'unknown user.'
                elif data[0][1] == 'L':
                    return 2, 'this user account was locked by system.'
                elif data[0][1] == 'S':
                    return 3, 'this user account was locked by user.'
                elif data[0][1] == 'E':
                    return 4, 'system account can not login.'
                elif data[0][1] == 'C' or data[0][1] == 'P':
                    if data[0][4] != 'T' and self._email_is_required:
                        return 6, 'please verify your email address. before login.'
                    elif not compare_digest(
                            data[0][5],
                            password if self._save_raw_password else sha256(password.encode()).hexdigest()
                    ):
                        await cursor.execute(MocaUsers._SAVE_LOGIN_LOG, (userid, ip, 'incorrect password.', 'F'))
                        await con.commit()
                        return 7, 'incorrect password.'
                    elif data[0][1] == 'P':
                        verification_code = uuid4().hex[:6]
                        await self._redis.save('moca-user-phone-login-' + userid,
                                               verification_code,
                                               600)
                        self._sms.send_sms(f'Your verification code is <{verification_code}> '
                                           f'Please enter your verification code in 10 minutes.', data[0][6])
                        return -1, 'verification code send to your phone.'
                    else:
                        await cursor.execute(MocaUsers._SAVE_LOGIN_LOG,
                                             (userid, ip, 'login success (login by password)', 'T'))
                        await con.commit()
                        access_token = await self._get_access_token(userid)
                        return 0, access_token
                else:
                    return 5, 'unknown user status.'

    async def send_phone_login_code(self, userid: str, phone: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        -1: phone format error.
        0: verification code send to your phone.
        1: unknown user.
        2: this user account was locked by system.
        3: this user account was locked by user.
        4: system account can not login.
        5: unknown user status.
        6: too quickly.
        7: please verify your email address. before login.
        8: please verify your phone number. before login.
        9: incorrect phone number.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if (not isinstance(phone, str)) or (len(phone) != 4):
            return -1, 'phone format error.'
        log = await self._redis.get('moca-send-phone-login-code-' + userid)
        if log is None:
            await self._redis.save(
                'moca-send-phone-login-code-' + userid, 'send', 60  # can send once per 60 seconds.
            )
        else:
            return 6, 'too quickly.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_LOGIN_INFO, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return 1, 'unknown user.'
                elif not compare_digest(data[0][6][-4:], phone):
                    return 9, 'incorrect phone number.'
                elif data[0][1] == 'L':
                    return 2, 'this user account was locked by system.'
                elif data[0][1] == 'S':
                    return 3, 'this user account was locked by user.'
                elif data[0][1] == 'E':
                    return 4, 'system account can not login.'
                elif data[0][1] == 'C' or data[0][1] == 'P':
                    if data[0][4] != 'T' and self._email_is_required:
                        return 7, 'please verify your email address. before login.'
                    elif data[0][6].startswith('F'):
                        return 8, 'please verify your phone number. before login.'
                    else:
                        verification_code = uuid4().hex[:6]
                        await self._redis.save('moca-user-phone-login-' + userid,
                                               verification_code,
                                               600)
                        self._sms.send_sms(f'Your verification code is <{verification_code}> '
                                           f'Please enter your verification code in 10 minutes.', data[0][6])
                        return 0, 'verification code send to your phone.'
                else:
                    return 5, 'unknown user status.'

    async def login_by_phone(self, userid: str, token: str, phone: str, ip: str = 'unknown') -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        -3: ip format error.
        -2: phone format error.
        -1: invalid verification code.
        1: unknown user.
        2: this user account was locked by system.
        3: this user account was locked by user.
        4: system account can not login.
        5: unknown user status.
        6: please verify your email address. before login.
        7: please setup your phone number, before login.
        8: token format error.
        9: incorrect phone number.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if (not isinstance(phone, str)) or (len(phone) != 4):
            return -2, 'phone format error.'
        if (not isinstance(token, str)) or (len(token) != 6):
            return 8, 'token format error.'
        if (not isinstance(ip, str)) or (len(ip) > 64):
            return -3, 'ip format error.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_LOGIN_INFO, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return 1, 'unknown user.'
                elif not compare_digest(data[0][6][-4:], phone):
                    return 9, 'incorrect phone number.'
                elif data[0][1] == 'L':
                    return 2, 'this user account was locked by system.'
                elif data[0][1] == 'S':
                    return 3, 'this user account was locked by user.'
                elif data[0][1] == 'E':
                    return 4, 'system account can not login.'
                elif data[0][1] == 'C' or data[0][1] == 'P':
                    if data[0][4] != 'T' and self._email_is_required:
                        return 6, 'please verify your email address. before login.'
                    else:
                        verification_code = str(await self._redis.get('moca-user-phone-login-' + userid))
                        if compare_digest(verification_code, token):
                            await cursor.execute(MocaUsers._SAVE_LOGIN_LOG,
                                                 (userid, ip, 'login success (login by phone)', 'T'))
                            await con.commit()
                            access_token = await self._get_access_token(userid)
                            await self._redis.delete('moca-user-phone-login-' + userid)
                            return 0, access_token
                        else:
                            await cursor.execute(
                                MocaUsers._SAVE_LOGIN_LOG,
                                (userid, ip, 'incorrect verification code(phone).', 'F')
                            )
                            await con.commit()
                            return -1, 'invalid verification code.'
                else:
                    return 5, 'unknown user status.'

    async def search_users_by_name(self, name: str) -> \
            Tuple[int, Union[str, List[Tuple[str, str, str, Any, Any, str]]]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <a list of user's info>
        1: name must be a string.
        2: name is too long.
        """
        if not isinstance(name, str):
            return 1, 'name must be a string.'
        elif len(name) > 512:
            return 2, 'name is too long.'
        cache = await self._redis.get('moca-search-users-by-name-cache-' + sha1(name.encode()).hexdigest())
        if cache is None:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    keywords = name.replace('　', ' ').split()
                    await cursor.execute(MocaUsers._SEARCH_USERS_BY_NAME, (f'%{keywords[0]}%',))
                    res = await cursor.fetchall()
                    if len(res) > 0:
                        if len(keywords) >= 2:
                            for keyword in keywords:
                                data = [(item[0], item[1], item[2], loads(item[3]), loads(item[4]), item[5])
                                        for item in res if keyword in item[1]]
                        else:
                            data = [(item[0], item[1], item[2], loads(item[3]), loads(item[4]), item[5])
                                    for item in res]
                        await self._redis.save(
                            'moca-search-users-by-name-cache-' + sha1(name.encode()).hexdigest(), data, 600
                            # 10 minutes
                        )
                        return 0, list(data)
                    else:
                        return 0, []
        else:
            return 0, cache

    async def search_user_by_id(self, userid: str) -> Tuple[int, Union[str, Tuple[str, str, str, Any, Any, str]]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <user info>
        1: unknown user id.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        cache = await self._redis.get('moca-search-user-by-id-cache-' + userid)
        if cache is None:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._SEARCH_USER_BY_ID, (userid,))
                    data = await cursor.fetchall()
                    if len(data) > 0:
                        await self._redis.save(
                            'moca-search-user-by-id-cache-' + userid, data[0], 600  # 10 minutes
                        )
                        return 0, (data[0][0], data[0][1], data[0][2], loads(data[0][3]), loads(data[0][4]), data[0][5])
                    else:
                        return 1, 'unknown user id.'
        else:
            return 0, cache

    async def search_users(self, keywords: List[str]) -> List[Tuple[str, str, str, Any, Any, str]]:
        """The maximum length of the keywords is 64, the maximum characters per keyword is 512."""
        if (not isinstance(keywords, list)) or (len(keywords) > 64):
            return []
        data: list = []
        for keyword in keywords:
            if len(keyword) <= 512:
                res = await self.search_users_by_name(keyword)
                if res[0] == 0:
                    data += res[1]
                res = await self.search_user_by_id(keyword)
                if res[0] == 0:
                    data += res[1]
            else:
                pass  # skip this keyword.
        return data

    async def save_profile(self, userid: str, profile: str, token: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: save profile successfully.
        1: incorrect token.
        2: profile too long.
        3: token format error.
        4: profile must be a string.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, token)
        if res[0] != 0:
            return res
        if not isinstance(profile, str):
            return 4, 'profile must be a string.'
        if len(profile) > 2048:
            return 2, 'profile too long.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._SAVE_PROFILE, (profile, userid))
                await con.commit()
                await self._redis.save(
                    'moca-user-profile-cache-' + userid, profile, 600  # 10 minutes
                )
                return 0, 'save profile successfully.'

    async def get_profile(self, userid: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <profile>
        1: unknown user.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        cache = await self._redis.get('moca-user-profile-cache-' + userid)
        if cache is None:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._GET_PROFILE, (userid,))
                    data = await cursor.fetchall()
                    if len(data) > 0:
                        await self._redis.save(
                            'moca-user-profile-cache-' + userid, str(data[0]), 600  # 10 minutes
                        )
                        return 0, str(data[0])
                    else:
                        return 1, 'unknown user.'
        else:
            return 0, cache

    async def get_profiles(self, userid_list: List[str]) -> List[Tuple[int, str]]:
        """The maximum length of userid_list is 64."""
        if (not isinstance(userid_list, list)) or (len(userid_list) > 64):
            return []
        else:
            return [await self.get_profile(userid) for userid in userid_list]

    @staticmethod
    def _check_phone_format(phone: str) -> bool:
        if not isinstance(phone, str):
            return False
        elif phone[0] != '+':
            return False
        for char in phone[1:]:
            if not char.isdigit():
                return False
        return True

    async def add_phone_number(self, userid: str, phone: str, access_token: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: phone number format error.
        3: token format error.
        4: too quickly.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if not self._check_phone_format(phone):
            return 2, 'phone number format error.'
        log = await self._redis.get('moca-send-phone-verification-' + userid)
        if log is not None:
            return 4, 'too quickly.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._UPDATE_PHONE, ('F' + phone, userid))
                await con.commit()
        verification_code = uuid4().hex[:6]
        await self._redis.save(
            'moca-add-phone-cache-' + userid,
            verification_code,
            600,  # 10 minutes.
        )
        await self._redis.save(
            'moca-send-phone-verification-' + userid, 'send', 60  # can send once per 60 seconds
        )
        self._sms.send_sms(f'Your verification code is <{verification_code}>. '
                           f'Please enter your verification code in 10 minutes.', phone)
        return 0, 'success.'

    async def verify_phone(self, userid: str, verification_code: str, access_token: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: incorrect verification code.
        3: token format error.
        4: already verified.
        5: too quickly.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        code = await self._redis.get('moca-add-phone-cache-' + userid)
        log = await self._redis.get('moca-phone-verification-' + userid)
        if log is None:
            await self._redis.save(
                'moca-phone-verification-' + userid, 'verify', 5  # can verify once per 5 seconds.
            )
        else:
            return 5, 'too quickly.'
        if (isinstance(verification_code, str)) and (len(verification_code) == 6)\
                and compare_digest(str(code), verification_code):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._GET_PHONE, (userid,))
                    phone = await cursor.fetchall()
                    if phone[0][0].startswith('F'):
                        await cursor.execute(MocaUsers._UPDATE_PHONE, (phone[0][0][1:], userid))
                        await con.commit()
                        return 0, 'success.'
                    else:
                        return 4, 'already verified.'
        else:
            return 2, 'incorrect verification code.'

    async def has_verified_phone(self, userid: str) -> bool:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return False
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_PHONE, (userid,))
                phone = await cursor.fetchall()
                if len(phone) > 0 and str(phone[0][0]).startswith('+'):
                    return True
                else:
                    return False

    async def check_password(self, userid: str, password: str) -> bool:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return False
        res = self._check_password_format(password)
        if res[0] != 0:
            return False
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(
                    MocaUsers._CHECK_PASSWORD,
                    (userid, password if self._save_raw_password else sha256(password.encode()).hexdigest())
                )
                data = await cursor.fetchall()
                if len(data) > 0:
                    return True
                else:
                    return False

    async def start_two_step_verification(self, userid: str, password: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect password.
        2: please setup your phone number.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if await self.check_password(userid, password):
            if await self.has_verified_phone(userid):
                pool = await self._mysql.get_aio_pool()
                async with pool.acquire() as con:
                    async with con.cursor() as cursor:
                        await cursor.execute(MocaUsers._UPDATE_STATUS, ('P', userid))
                        await con.commit()
                        return 0, 'success.'
            else:
                return 2, 'please setup your phone number.'
        else:
            return 1, 'incorrect password.'

    async def stop_two_step_verification(self, userid: str, password: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect password.
        2: please setup your phone number.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if await self.check_password(userid, password):
            if await self.has_verified_phone(userid):
                pool = await self._mysql.get_aio_pool()
                async with pool.acquire() as con:
                    async with con.cursor() as cursor:
                        await cursor.execute(MocaUsers._UPDATE_STATUS, ('C', userid))
                        await con.commit()
                        return 0, 'success.'
            else:
                return 2, 'please setup your phone number.'
        else:
            return 1, 'incorrect password.'

    async def check_system_account_permission(self, userid: str, password: str, permission: str) -> bool:
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return False
        res = self._check_password_format(password)
        if res[0] != 0:
            return False
        if (not isinstance(permission, str)) or (len(permission) > 32):
            return False
        pool = await self._mysql.get_aio_pool()
        cache = await self._redis.get(f'system-account-permission-{userid}-{sha256(password.encode()).hexdigest()}')
        if cache is None:
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(
                        MocaUsers._GET_PERMISSION,
                        (userid, password if self._save_raw_password else sha256(password.encode()).hexdigest())
                    )
                    data = await cursor.fetchall()
                    await self._redis.save(
                        f'system-account-permission-{userid}-{sha256(password.encode()).hexdigest()}',
                        data,
                    )
        else:
            data = cache
        try:
            if '-RT-' in data[0][0]:
                return True
            for tmp in permission.upper().split('|'):
                if tmp in data[0][0]:
                    return True
            return False
        except IndexError:
            return False

    async def get_my_login_log(self, userid: str, access_token: str) -> Tuple[int, Union[str, List[str]]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <login log>
        1: incorrect token.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_LOGIN_LOG, (userid,))
                data = await cursor.fetchall()
                return 0, list(data)

    async def get_user_access_token(self, userid: str, password: str, target_userid: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: access token
        1: permission denied.
        2: target userid format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        res = self._check_userid_format(target_userid)
        if res[0] != 0:
            return 2, 'target userid format error.'
        if await self.check_system_account_permission(userid, password, '-MU-'):
            return 0, await self._get_access_token(target_userid)
        else:
            return 1, 'permission denied.'

    async def lock_my_account(self, userid: str, password: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect password.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        if await self.check_password(userid, password):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._UPDATE_STATUS, ('S', userid))
                    await con.commit()
                    return 0, 'success.'
        else:
            return 1, 'incorrect password.'

    async def lock_user_account(self, userid: str, password: str, target_userid: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect password or permission.
        2: target userid format error.
        60: user id must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        res = self._check_userid_format(target_userid)
        if res[0] != 0:
            return 2, 'target userid format error.'
        if await self.check_system_account_permission(userid, password, '-MU-|-RT-'):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._UPDATE_STATUS, ('L', target_userid))
                    await con.commit()
                    return 0, 'success.'
        else:
            return 1, 'incorrect password or permission.'

    async def reset_user_database(self) -> None:
        """This method will clear all database created by MocaUsers."""
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._DROP_DB)
                await con.commit()
        await self.init_db()

    async def save_user_image(self, userid: str, access_token: str, key: str, image: bytes) -> Tuple[int, str]:
        """
        This method will convert image to JPEG.
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: image format error.
        3: token format error.
        4: image size is too large.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if len(image) > 10485760:  # 10 MB
            return 4, 'image size is too large.'
        if len(key) > 64:
            return 4, 'key is too long.'
        _key = key.replace('.', 'dot').replace('/', 'slash')
        path = self._users_dir.joinpath(userid).joinpath('image')
        path.mkdir(parents=True, exist_ok=True)
        filename = str(path.joinpath(add_dot_jpg(_key)))
        try:
            with Image.open(BytesIO(image)) as src:
                data = src.getdata()
                mode = src.mode
                size = src.size
        except UnidentifiedImageError:
            return 2, 'image format error.'
        with Image.new(mode, size) as dst:
            dst.putdata(data)
            dst = dst.convert('RGB')
            dst.save(str(filename), 'JPEG', quality=90)
        return 0, 'success.'

    async def get_user_image(self, userid: str, access_token: str, key: str) -> Tuple[int, Union[str, bytes]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <image data>
        1: incorrect token.
        2: unknown data.
        3: token format error.
        4: key is too long.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if len(key) > 64:
            return 4, 'key is too long.'
        _key = key.replace('.', 'dot').replace('/', 'slash')
        filename = str(self._users_dir.joinpath(userid).joinpath('image').joinpath(add_dot_jpg(_key)))
        try:
            async with open(str(filename), mode='rb') as file:
                data = await file.read()
                return 0, data
        except FileNotFoundError:
            return 2, 'unknown data.'

    async def save_big_icon(self, userid: str, access_token: str, icon: bytes) -> Tuple[int, str]:
        """
        This method will convert image to JPEG.
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        return await self.save_user_image(userid, access_token, 'moca-user-icon-big', icon)

    async def get_big_icon(self, userid: str, access_token: str) -> Tuple[int, Union[str, bytes]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <image data>
        1: incorrect token.
        2: unknown data.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        return await self.get_user_image(userid, access_token, 'moca-user-icon-big')

    async def save_small_icon(self, userid: str, access_token: str, icon: bytes) -> Tuple[int, str]:
        """
        This method will convert image to JPEG.
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        return await self.save_user_image(userid, access_token, 'moca-user-icon-small', icon)

    async def get_small_icon(self, userid: str, access_token: str) -> Tuple[int, Union[str, bytes]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <image data>
        1: incorrect token.
        2: unknown data.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        return await self.get_user_image(userid, access_token, 'moca-user-icon-small')

    async def save_user_file(self, userid: str, access_token: str, key: str, data: bytes) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        3: token format error.
        4: key format error.
        5: key is too long.
        6: data is too large.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        if not isinstance(key, str):
            return 4, 'key format error.'
        elif len(key) > 64:
            return 5, 'key is too long.'
        elif len(data) > 268435456:  # 256 MB
            return 6, 'data is too large.'
        _key = key.replace('.', 'dot').replace('/', 'slash')
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        path = self._users_dir.joinpath(userid).joinpath('file')
        path.mkdir(parents=True, exist_ok=True)
        filename = str(path.joinpath(_key))
        async with open(filename, mode='wb') as file:
            await file.write(compress(data))
            return 0, 'success.'

    async def get_user_file(self, userid: str, access_token: str, key: str,
                            auto_decompress: bool = True) -> Tuple[int, Union[str, bytes]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <data>
        1: incorrect token.
        2: unknown data.
        3: token format error.
        4: key format error.
        5: key is too long.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        if not isinstance(key, str):
            return 4, 'key format error.'
        elif len(key) > 64:
            return 5, 'key is too long.'
        _key = key.replace('.', 'dot').replace('/', 'slash')
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        filename = str(self._users_dir.joinpath(userid).joinpath('file').joinpath(_key))
        try:
            async with open(filename, mode='rb') as file:
                data = await file.read()
                if auto_decompress:
                    return 0, decompress(data)
                else:
                    return 0, data
        except FileNotFoundError:
            return 2, 'unknown data.'

    async def send_message(self, from_: str, to_: str, access_token: str, message: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: unknown target userid.
        3: token format error.
        4: message is too long.
        5: message format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        if not isinstance(message, str):
            return 5, 'message format error.'
        elif len(message) > 8192:
            return 4, 'message is too long.'
        res = await self.check_access_token(from_, access_token)
        if res[0] != 0:
            return res
        status = await self.check_userid(to_)
        if status[0] == 1:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._SEND_MESSAGE, (from_, to_, message))
                    await con.commit()
                    return 0, 'success.'
        else:
            return 2, 'unknown target userid.'

    async def get_messages(self, userid: str, access_token: str, start: int, limit: int) \
            -> Tuple[int, Union[str, List[Tuple[int, str, str, datetime]]]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <message list>
        1: incorrect token.
        2: invalid start or limit parameter.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        if (not isinstance(start, int)) or (not isinstance(limit, int)) or (start < 0) or (limit < 0):
            return 2, 'invalid start or limit parameter.'
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_MESSAGES, (userid,))
                data = await cursor.fetchall()
                if len(data) > 0:
                    return 0, list(data)
                else:
                    return 0, []

    async def change_password(self, userid: str, old: str, new: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: failed.
        2: new password format error.
        """
        if not self._check_password_format(new):
            return 2, 'new password format error.'
        if await self.check_password(userid, old):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._UPDATE_PASS, (new, userid))
                    await con.commit()
                    return 0, 'success.'
        else:
            return 1, 'failed.'

    async def has_verified_email(self, userid: str) -> bool:
        if not self._check_userid_format(userid):
            return False
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_EMAIL, (userid,))
                data = await cursor.fetchall()
                if len(data) == 0:
                    return False
                elif data[0][1] == 'T':
                    return True
                else:
                    return False

    async def get_user_email_list(self, userid_list: List[str]) -> List[Tuple[str, str]]:
        """The maximum length of userid_list is 1024."""
        if (not isinstance(userid_list, list)) or (len(userid_list) > 1024):
            return []
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                result: List[Tuple[str, str]] = []
                for userid in userid_list:
                    if self._check_userid_format(userid):
                        await cursor.execute(MocaUsers._GET_EMAIL, (userid,))
                        data = await cursor.fetchall()
                        if len(data) > 0 and data[0][1] == 'T':
                            result.append((userid, data[0][0]))
                    else:
                        pass  # skip the userid.
                return result

    async def send_email_to_users(self, userid_list: List[str], title: str, body: str, type_='html') -> List[str]:
        """
        Return a list of users that can receive E-Mail notifications successfully.
        The maximum length of title is 32, the maximum length of body is 1024.
        The maximum length of userid_list is 1024.
        """
        if (not isinstance(title, str)) or (not isinstance(body, str)) or (type_ not in ('html', 'plain')) \
                or (len(title) > 32) or (len(body) > 1024) or (not isinstance(userid_list, list))\
                or (len(userid_list) > 1024):
            return []
        email_list: List[Tuple[str, str]] = await self.get_user_email_list(userid_list)
        success_list: List[str] = []
        for email_info in email_list:
            try:
                await self._mail.send_aio_mail(email_info[1], body, title, type_)
                success_list.append(email_info[0])
            except SMTPException:
                pass
        return success_list

    async def get_user_phone_number(self, userid_list: List[str]) -> List[Tuple[str, str]]:
        """The maximum length of userid_list is 1024."""
        if (not isinstance(userid_list, list)) or (len(userid_list) > 1024):
            return []
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                result: List[Tuple[str, str]] = []
                for userid in userid_list:
                    if self._check_userid_format(userid):
                        await cursor.execute(MocaUsers._GET_PHONE, (userid,))
                        data = await cursor.fetchall()
                        if len(data) > 0 and isinstance(data[0][0], str) and data[0][0].startswith('+'):
                            result.append((userid, data[0][0]))
                    else:
                        pass  # skip this id.
                return result

    async def send_sms_to_users(self, userid_list: List[str], body: str) -> List[str]:
        """
        Return a list of users that can receive SMS notifications successfully.
        The maximum length of the body is 1024.
        The maximum length of userid_list is 64.
        """
        if (not isinstance(userid_list, list)) or (not isinstance(body, str)) \
                or (len(body) > 1024) or (len(userid_list) > 64):
            return []
        phone_list: List[Tuple[str, str]] = await self.get_user_phone_number(userid_list)
        success_list: List[str] = []
        for phone_info in phone_list:
            try:
                self._sms.send_sms(body, phone_info[1])
                success_list.append(phone_info[0])
            except TwilioException:
                pass
        return success_list

    async def forgot_password(self, userid: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        -1: need a valid email or phone number.
        0: send email successfully.
        1: send sms successfully.
        2: send email failed.
        3: send sms failed.
        """
        key = uuid4().hex[:6]
        await self._redis.save('moca-forgot-password-' + userid, key, 600)  # 10 minutes
        if await self.has_verified_email(userid):
            body = MocaUsers.FORGOT_PASS_BODY % key
            res = await self.send_email_to_users([userid], MocaUsers.FORGOT_PASS_TITLE, body)
            if userid in res:
                return 0, 'send email successfully.'
            else:
                return 2, 'send email failed.'
        elif await self.has_verified_phone(userid):
            res = await self.send_sms_to_users(
                [userid],
                f'Your verification code is <{key}>. Please enter your verification code in 10 minutes.'
            )
            if userid in res:
                return 1, 'send sms successfully.'
            else:
                return 3, 'send sms failed.'
        else:
            return -1, 'need a valid email or phone number.'

    async def reset_password(self, userid: str, password: str, verification_code: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: invalid verification code.
        50: password must be a string.
        51: password length error.
        52: password must contains a alphabet.
        53: password must contains a number.
        54: password must contains a symbol.
        55: password must only contains ascii characters.
        56: password must contains upper case characters.
        57: password must contain lower case characters.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = self._check_userid_format(userid)
        if res[0] != 0:
            return res
        res = self._check_password_format(password)
        if res[0] != 0:
            return res
        key = await self._redis.get('moca-forgot-password-' + userid)
        if (key is None) or (not isinstance(verification_code, str)) or (verification_code != key):
            return 1, 'invalid verification code.'
        else:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._UPDATE_PASS, (password, userid))
                    await con.commit()
                    return 0, 'success.'

    async def save_my_user_data(self, userid: str, access_token: str, storage: int, data: Any) -> Tuple[int, str]:
        """
        storage 0, 1 is public storage. 2, 3, 4, 5, 6, 7 is private storage.
        Return: status_code, response_message.
        Status Code
        -----------
        -1: data is too long.
        0: success.
        1: incorrect token.
        2: invalid storage id.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if storage not in (0, 1, 2, 3, 4, 5, 6, 7):
            return 2, 'invalid storage id.'
        try:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._SAVE_USER_DATA, (storage, dumps(data), userid))
                    await con.commit()
                    await self._redis.save(
                        f'moca-storage{storage}-cache-{userid}',
                        data,
                        600  # 10 minutes.
                    )
                    return 0, 'success.'
        except DataError:
            return -1, 'data is too long.'

    async def get_my_user_data(self, userid: str, access_token: str, storage: int) -> Tuple[int, Any]:
        """
        storage 0, 1 is public storage. 2, 3, 4, 5, 6, 7 is private storage.
        Return: status_code, response_message.
        Status Code
        -----------
        0: <data>.
        1: incorrect token.
        2: invalid storage id.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if storage not in (0, 1, 2, 3, 4, 5, 6, 7):
            return 2, 'invalid storage id.'
        cache = await self._redis.get(f'moca-storage{storage}-cache-{userid}')
        if cache is not None:
            return 0, cache
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_USER_DATA, (storage, userid))
                res = await cursor.fetchall()
                if len(res) > 0:
                    data = loads(res[0][0])
                    if len(res[0][0]) < 4096:
                        await self._redis.save(
                            f'moca-storage{storage}-cache-{userid}',
                            data,
                            600  # 10 minutes.
                        )
                    return 0, data
                else:
                    return 0, None

    async def get_other_user_data(self, userid: str, access_token: str,
                                  target_userid: str, storage: int) -> Tuple[int, Any]:
        """
        storage 0, 1 is public storage. 2, 3, 4, 5, 6, 7 is private storage.
        Return: status_code, response_message.
        Status Code
        -----------
        -1: permission denied.
        0: <data>.
        1: incorrect token.
        2: invalid storage id.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if storage not in (0, 1, 2, 3, 4, 5, 6, 7):
            return 2, 'invalid storage id.'
        elif (storage not in (0, 1)) and (not await self.check_system_account_permission(userid, access_token, '-MU-')):
            return -1, 'permission denied.'
        return await self.get_my_user_data(
            target_userid, await self._get_access_token(target_userid), storage
        )

    async def save_other_user_data(self, userid: str, access_token: str,
                                   target_userid: str, storage: int, data: Any) -> Tuple[int, str]:
        """
        storage 0, 1 is public storage. 2, 3, 4, 5, 6, 7 is private storage.
        Return: status_code, response_message.
        Status Code
        -----------
        -2: permission denied.
        -1: data is too long.
        0: success.
        1: incorrect token.
        2: invalid storage id.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if storage not in (0, 1, 2, 3, 4, 5, 6, 7):
            return 2, 'invalid storage id.'
        elif (storage not in (0, 1)) and (not await self.check_system_account_permission(userid, access_token, '-MU-')):
            return -2, 'permission denied.'
        return await self.save_my_user_data(
            target_userid, await self._get_access_token(target_userid), storage, data
        )

    async def get_user_count(self) -> int:
        """Return the number of users."""
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_USER_NUMBER)
                res = await cursor.fetchall()
                return res[0][0]

    async def get_locked_user_number(self) -> int:
        """Return the number of users that was locked."""
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._GET_LOCKED_USER_NUMBER)
                res = await cursor.fetchall()
                return res[0][0]

    async def get_users_list(self, userid: str, password: str, start: int, limit: int)\
            -> List[Tuple[str, str, str, str, str, str, datetime]]:
        """Return users list. (id, status, name, email, email_verified, phone, created_at)"""
        if not isinstance(start, int) or not isinstance(limit, int) or start < 0 or limit < 0:
            return []
        elif await self.check_system_account_permission(userid, password, '-MU-'):
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._GET_USERS_LIST, (start, limit))
                    res = await cursor.fetchall()
                    return list(res)
        else:
            return []

    async def insert_data_to_storage(self, userid: str, access_token: str, key: str, data: Any) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: your data is too large.
        3: token format error.
        4: key is too long.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(key, str)) or (len(key) > 64):
            return 4, 'key is too long.'
        try:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._INSERT_DATA_TO_STORAGE, (userid, key, dumps(data)))
                    await con.commit()
            return 0, 'success.'
        except DataError:
            return 2, 'your data is too large.'

    async def select_data_from_storage(self, userid: str,
                                       access_token: str, key: str) -> Tuple[int, Any]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <data>
        1: incorrect token.
        3: token format error.
        4: key is too long.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(key, str)) or (len(key) > 64):
            return 4, 'key is too long.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._SELECT_DATA_FROM_STORAGE, (userid, key))
                data = await cursor.fetchall()
                return 0, [(item[0], loads(item[1]), item[2]) for item in data]

    async def delete_data_from_storage_by_id(self, userid: str, access_token: str, content_id: int) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: content_id format error.
        3: token format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(content_id, int)) or (content_id < 0):
            return 2, 'content_id format error.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._DELETE_DATA_FROM_STORAGE_BY_ID, (userid, content_id))
                await con.commit()
                return 0, 'success.'

    async def delete_data_from_storage_by_key(self, userid: str, access_token: str, key: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        3: token format error.
        4: key is too long.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(key, str)) or (len(key) > 64):
            return 4, 'key is too long.'
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaUsers._DELETE_DATA_FROM_STORAGE_BY_KEY, (userid, key))
                await con.commit()
                return 0, 'success.'

    async def update_data_in_storage_by_id(self, userid: str,
                                           access_token: str, content_id: int, data: Any) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: your data is too large.
        3: token format error.
        4: content_id format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(content_id, int)) or (content_id < 0):
            return 2, 'content_id format error.'
        try:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaUsers._UPDATE_DATA_IN_STORAGE, (dumps(data), userid, content_id))
                    await con.commit()
            return 0, 'success.'
        except DataError:
            return 2, 'your data is too large.'

    async def share_file(self, userid: str, access_token: str, filename: str, data: bytes, protection: str = '',
                         time_limit: int = 0, info: str = '') -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <access key>
        1: incorrect token.
        2: your data is too large.
        3: token format error.
        4: protection format error.
        5: filename is too long.
        6: time limit format error.
        7: info format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if len(data) > 4294967296:  # 4 GB
            return 2, 'your data is too large.'
        if (not isinstance(filename, str)) or (len(filename) > 256):
            return 5, 'filename is too long.'
        if (not isinstance(protection, str)) or (len(protection) > 64):
            return 4, 'protection format error.'
        if (not isinstance(time_limit, int)) or (time_limit < 0):
            return 6, 'time limit format error.'
        if (not isinstance(info, str)) or (len(info) > 4096):
            return 7, 'info format error.'
        key = uuid4().hex
        path = self._users_dir.joinpath('shared_files').joinpath(key)
        path.mkdir(parents=True, exist_ok=True)
        async with open(str(path.joinpath('data')), mode='wb') as data_file:
            await data_file.write(compress(data))
        async with open(str(path.joinpath('info.json')), mode='w', encoding='utf-8') as info_file:
            await info_file.write(json_dumps({
                'user_id': userid,
                'protection': protection if self._save_raw_password else sha256(protection.encode()).hexdigest(),
                'filename': filename,
                'time_limit': datetime.now(tz).timestamp() + time_limit if time_limit != 0 else 0,
                'info': info,
            }))
        return 0, key

    async def get_shared_file(self, key: str, protection: str = '') -> Tuple[int, Union[str, Tuple[bytes, str, str]]]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <data, filename, info>
        1: time out.
        2: file not found.
        3: key format error.
        4: protection format error.
        5: incorrect password.
        """
        if (not isinstance(protection, str)) or (len(protection) > 64):
            return 4, 'protection format error.'
        if (not isinstance(key, str)) or (len(key) != 32):
            return 3, 'key format error.'
        path = self._users_dir.joinpath('shared_files').joinpath(key)
        try:
            async with open(str(path.joinpath('info.json')), mode='r', encoding='utf-8') as info_file:
                info = json_loads(await info_file.read())
            if (info['time_limit'] != 0) and (datetime.now(tz).timestamp() > info['time_limit']):
                return 1, 'time out.'
            if info['protection'] != protection if self._save_raw_password else sha256(protection.encode()).hexdigest():
                return 5, 'incorrect password.'
            async with open(str(path.joinpath('data')), mode='rb') as data_file:
                return 0, (decompress(await data_file.read()), info['filename'], info['info'])
        except FileNotFoundError:
            return 2, 'file not found.'

    async def change_shared_file_info(self, userid: str, access_token: str, key: str, info: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: key format error.
        3: token format error.
        4: permission denied.
        5: file not found.
        7: info format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if (not isinstance(info, str)) or (len(info) > 4096):
            return 7, 'info format error.'
        if(not isinstance(key, str)) or (len(key) != 32):
            return 3, 'key format error.'
        path = self._users_dir.joinpath('shared_files').joinpath(key)
        try:
            async with open(str(path.joinpath('info.json')), mode='r', encoding='utf-8') as info_file:
                json_data = json_loads(await info_file.read())
                if json_data['user_id'] == userid:
                    json_data['info'] = info
                else:
                    return 4, 'permission denied.'
            async with open(str(path.joinpath('info.json')), mode='w', encoding='utf-8') as info_file:
                await info_file.write(json_dumps(json_data))
        except FileNotFoundError:
            return 5, 'file not found.'
        return 0, 'success.'

    async def change_shared_file_protection(self, userid: str, access_token: str,
                                            key: str, protection: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: key format error.
        3: token format error.
        4: permission denied.
        5: file not found.
        6: protection format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if(not isinstance(key, str)) or (len(key) != 32):
            return 3, 'key format error.'
        if (not isinstance(protection, str)) or (len(protection) > 64):
            return 6, 'protection format error.'
        path = self._users_dir.joinpath('shared_files').joinpath(key)
        try:
            async with open(str(path.joinpath('info.json')), mode='r', encoding='utf-8') as info_file:
                json_data = json_loads(await info_file.read())
                if json_data['user_id'] == userid:
                    json_data['protection'] = protection
                else:
                    return 4, 'permission denied.'
            async with open(str(path.joinpath('info.json')), mode='w', encoding='utf-8') as info_file:
                await info_file.write(json_dumps(json_data))
        except FileNotFoundError:
            return 5, 'file not found.'
        return 0, 'success.'

    async def change_shared_file_time_limit(self, userid: str, access_token: str,
                                            key: str, time_limit: int) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: incorrect token.
        2: key format error.
        3: token format error.
        4: permission denied.
        5: file not found.
        6: time limit format error.
        60: userid must be a string.
        61: user id length error.
        63: user is must only contains ascii characters.
        """
        res = await self.check_access_token(userid, access_token)
        if res[0] != 0:
            return res
        if(not isinstance(key, str)) or (len(key) != 32):
            return 3, 'key format error.'
        if (not isinstance(time_limit, int)) or (time_limit < 0):
            return 6, 'time limit format error.'
        path = self._users_dir.joinpath('shared_files').joinpath(key)
        try:
            async with open(str(path.joinpath('info.json')), mode='r', encoding='utf-8') as info_file:
                json_data = json_loads(await info_file.read())
                if json_data['user_id'] == userid:
                    json_data['time_limit'] = datetime.now(tz).timestamp() + time_limit if time_limit != 0 else 0
                else:
                    return 4, 'permission denied.'
            async with open(str(path.joinpath('info.json')), mode='w', encoding='utf-8') as info_file:
                await info_file.write(json_dumps(json_data))
        except FileNotFoundError:
            return 5, 'file not found.'
        return 0, 'success.'

# -------------------------------------------------------------------------- MocaUsers --
