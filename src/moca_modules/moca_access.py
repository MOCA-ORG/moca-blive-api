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

from .moca_base_class import MocaClassCache, MocaNamedInstance
from .moca_redis import MocaRedis
from .moca_mysql import MocaMysql
from .moca_random import get_random_string
from typing import *
from sanic.request import Request
from limits import parse_many
from limits.strategies import FixedWindowElasticExpiryRateLimiter
from limits.storage import RedisStorage

# -------------------------------------------------------------------------- Imports --

# -- MocaAccess --------------------------------------------------------------------------


class MocaAccess(MocaClassCache, MocaNamedInstance):
    """
    A access control class.

    Attributes
    ----------
    _redis: MocaRedis
        a instance of MocaRedis.
    _mysql: MocaMysql
        a instance of MocaMysql.
    _redis_storage: RedisStorage
        a redis storage for rate limit module.
    _api_key_window: FixedWindowElasticExpiryRateLimiter
        the window object used by rate limit.
    _ip_window: FixedWindowElasticExpiryRateLimiter
        the window object used by rate limit.
    _sync_count: int
        the is a count down timer to save redis value to mysql.
    _global_rate_limit
        the ip rate limit.
    """

    _API_KEY_TABLE = """
    create table if not exists moca_api_keys (
        api_key varchar(256) primary key,
        referer varchar(32) not null,
        rate_limit varchar(256) not null,
        access_limit bigint not null,
        count bigint not null,
        permission varchar(64) not null
    );
    """

    _CREATE_NEW_KEY = """
    insert into moca_api_keys(api_key, referer, rate_limit, access_limit, count, permission)
    values(%s,%s,%s,%s,%s,%s);
    """

    _GET_API_KEY_INFO = """
    select api_key, referer, rate_limit, access_limit, count, permission from moca_api_keys where api_key = %s;
    """

    _UPDATE_COUNT = """
    update moca_api_keys set count = %s where api_key = %s;
    """

    _REMOVE_API_KEY = """
    delete from moca_api_keys where api_key = %s;
    """

    def __init__(self, redis: MocaRedis, mysql: MocaMysql, global_rate_limit: str):
        MocaNamedInstance.__init__(self)
        MocaClassCache.__init__(self)
        self._redis: MocaRedis = redis
        self._mysql: MocaMysql = mysql
        self._redis_storage: RedisStorage = self._redis.get_redis_storage()
        self._api_key_window: FixedWindowElasticExpiryRateLimiter = FixedWindowElasticExpiryRateLimiter(
            self._redis_storage
        )
        self._ip_window: FixedWindowElasticExpiryRateLimiter = FixedWindowElasticExpiryRateLimiter(
            self._redis_storage
        )
        self._sync_count: int = 64
        self._global_rate_limit = parse_many(global_rate_limit)

    async def init_db(self) -> None:
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaAccess._API_KEY_TABLE)
                await con.commit()

    @staticmethod
    def _check_referer_format(referer: str) -> bool:
        if isinstance(referer, str) and (len(referer) <= 32):
            return True
        else:
            return False

    @staticmethod
    def _check_rate_limit_format(limit: str) -> bool:
        if isinstance(limit, str) and (len(limit) <= 256):
            try:
                if limit != '*':
                    parse_many(limit)
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def _check_access_limit_format(limit: int) -> bool:
        if isinstance(limit, int) and (limit >= -1):
            return True
        else:
            return False

    @staticmethod
    def _check_permission_format(permission: str) -> bool:
        if isinstance(permission, str) and (len(permission) <= 64):
            return True
        else:
            return False

    @staticmethod
    def _check_api_key_format(api_key: str) -> bool:
        if isinstance(api_key, str) and (len(api_key) == 256):
            return True
        else:
            return False

    @staticmethod
    def get_remote_address(request: Request) -> str:
        return request.remote_addr if request.remote_addr != '' else request.ip

    async def create_new_api_key(self, referer: str, rate_limit: str,
                                 access_limit: int, permission: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: <api key>
        1: referer format error.
        2: rate limit format error.
        3: access limit format error.
        4: permission format error.
        """
        if not self._check_referer_format(referer):
            return 1, 'referer format error.'
        if not self._check_rate_limit_format(rate_limit):
            return 2, 'rate limit format error.'
        if not self._check_access_limit_format(access_limit):
            return 3, 'access limit format error.'
        if not self._check_permission_format(permission):
            return 4, 'permission format error.'
        api_key = get_random_string(256)
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(MocaAccess._CREATE_NEW_KEY, (
                    api_key,
                    referer,
                    rate_limit,
                    access_limit,
                    0,
                    permission,
                ))
                await con.commit()
                return 0, api_key

    async def remove_api_key(self, api_key: str) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        0: success.
        1: unknown api key.
        """
        pool = await self._mysql.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cursor:
                res = await cursor.execute(MocaAccess._REMOVE_API_KEY, (api_key,))
                await con.commit()
                if res == 1:
                    await self._redis.delete('moca-api-key-cache-' + api_key)
                    return 0, 'success.'
                else:
                    return 1, 'unknown api key.'

    async def check_api_key(self, api_key: str, permission: str, request: Request) -> Tuple[int, str]:
        """
        Return: status_code, response_message.
        Status Code
        -----------
        -1: unknown api key.
        0: allowed.
        1: api_key format error.
        2: invalid referer.
        3: too many requests.
        4: you reached the access limit.
        5: permission error.
        """
        if not self._check_api_key_format(api_key):
            return 1, 'api_key format error.'
        cache = await self._redis.get('moca-api-key-cache-' + api_key)
        if cache is None:
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaAccess._GET_API_KEY_INFO, (api_key,))
                    res = await cursor.fetchall()
                    if len(res) > 0:
                        data = res[0]
                        data[2] = parse_many(data[2])
                        await self._redis.save('moca-api-key-cache-' + api_key, data)
                    else:
                        return -1, 'unknown api key.'
        else:
            data = cache
        referer = str(request.headers.get('referer', request.headers.get('origin')))
        if (data[1] != '*') and (not referer.startswith(data[1])):
            return 2, 'invalid referer.'
        if data[2] != '*':
            for item in data[2]:
                if not self._api_key_window.hit(item, self.get_remote_address(request)):
                    return 3, 'too many requests.'
        count = await self._redis.increment('moca-api-key-count-' + api_key)
        if self._sync_count >= 0:
            self._sync_count -= 1
        else:
            self._sync_count = 64
            pool = await self._mysql.get_aio_pool()
            async with pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(MocaAccess._UPDATE_COUNT, (count, api_key))
                    await con.commit()
        if count > data[3]:
            return 4, 'you reached the access limit.'
        if permission not in data[5]:
            return 5, 'permission error.'
        return 0, 'allowed.'

    def check_ip_rate_limit(self, request: Request, key: str = '') -> bool:
        for item in self._global_rate_limit:
            if not self._ip_window.hit(item, self.get_remote_address(request), key):
                return False
        return True

    def ip_hit(self, key: str) -> bool:
        for item in self._global_rate_limit:
            if not self._ip_window.hit(item, key):
                return False
        return True

    def rate_limit(self, limit: str, request: Request, key: str = '') -> bool:
        for item in parse_many(limit):
            if not self._ip_window.hit(item, self.get_remote_address(request), key):
                return False
        return True

# -------------------------------------------------------------------------- MocaAccess--
