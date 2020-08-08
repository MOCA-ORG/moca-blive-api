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
from pymysql import Connection
from pymysql.err import MySQLError
from aiomysql import connect, create_pool
from .moca_base_class import MocaNamedInstance, MocaClassCache

# -------------------------------------------------------------------------- Imports --

# -- Moca Mysql --------------------------------------------------------------------------


class MocaMysql(MocaClassCache, MocaNamedInstance):
    """
    mysql database.

    Attributes
    ----------
    _host: str
        database host ip.
    _port: int
        database port number.
    _user: str
        database user name.
    _password: str
        database password.
    _dbname: str
        database name.
    _min: int
        the minimum size of the connection pool.
    _max: int
        the maximum size of the connection pool.
    _con
        a database connection.
    _aio_con
        a async database connection.
    _aio_pool
        a async database connection pool.
    """

    def __init__(self, host: str, port: int, user: str, password: str,
                 dbname: str, minsize: int = 1, maxsize: int = 10):
        """
        :param host: database host ip.
        :param port: database port number.
        :param user: database user name.
        :param password: database password.
        :param dbname: database name.
        :param minsize: the minimum size of the connection pool.
        :param maxsize: the maximum size of the connection pool.
        """
        MocaNamedInstance.__init__(self)
        MocaClassCache.__init__(self)
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._dbname: str = dbname
        self._min: int = minsize
        self._max: int = maxsize
        self._con = Connection(host=host,
                               port=port,
                               user=user,
                               password=password,
                               db=dbname)
        self._aio_con = None
        self._aio_pool = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def user(self) -> str:
        return self._user

    @property
    def dbname(self) -> str:
        return self._dbname

    def get_con(self):
        """Get a connection."""
        return self._con

    def get_new_con(self):
        """Get a new connection."""
        self._con = Connection(host=self._host,
                               port=self._port,
                               user=self._user,
                               password=self._password,
                               db=self._dbname)
        return self._con

    async def get_aio_con(self):
        """Get a async connection."""
        if self._aio_con is None:
            con = await connect(host=self._host,
                                port=self._port,
                                user=self._user,
                                password=self._password,
                                db=self._dbname)
        else:
            con = self._aio_con
        return con

    async def get_new_aio_con(self):
        """Get a new async connection."""
        con = await connect(host=self._host,
                            port=self._port,
                            user=self._user,
                            password=self._password,
                            db=self._dbname)
        self._aio_con = con
        return con

    async def get_aio_pool(self):
        """Get a async connection pool."""
        if self._aio_pool is None:
            pool = await create_pool(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                     db=self._dbname,
                                     minsize=self._min,
                                     maxsize=self._max)
        else:
            pool = self._aio_pool
        return pool

    async def get_new_aio_pool(self):
        """Get a new async connection pool."""
        pool = await create_pool(host=self._host,
                                 port=self._port,
                                 user=self._user,
                                 password=self._password,
                                 db=self._dbname,
                                 minsize=self._min,
                                 maxsize=self._max)
        self._aio_pool = pool
        return pool

    def execute(self, query: str, param: Tuple):
        """Execute the query."""
        con = self.get_con()
        cursor = con.cursor()
        cursor.execute(query, args=param)
        con.commit()
        try:
            return cursor.fetchall()
        except MySQLError:
            return None

    async def execute_aio(self, query: str, param: Tuple):
        pool = await self.get_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(query, args=param)
                data = await cur.fetchall()
                await con.commit()
                return data

# -------------------------------------------------------------------------- Moca Mysql --
