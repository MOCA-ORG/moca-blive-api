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
from .variables import insert_comment, insert_gift, select_comments, select_gifts

# -------------------------------------------------------------------------- Imports --

# -- Query --------------------------------------------------------------------------


async def save_comment(pool, room_id: str, user: str, comment: str) -> None:
    async with pool.acquire() as con:
        async with con.cursor() as cur:
            await cur.execute(insert_comment, (room_id, user, comment))
            await con.commit()


async def save_gift(pool, room_id: str, user_name: str, gift_id: int, gift_name: str,
                    gift_num: int, coin_type: str, total_coin: int) -> None:
    async with pool.acquire() as con:
        async with con.cursor() as cur:
            await cur.execute(insert_gift, (room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin))
            await con.commit()


async def get_comments(pool, room_id: str, start: int, limit: int) -> List:
    async with pool.acquire() as con:
        async with con.cursor() as cur:
            await cur.execute(select_comments, (room_id, start, limit))
            data = await cur.fetchall()
            return [(*item[:-1], str(item[-1])) for item in data]


async def get_gifts(pool, room_id: str, start: int, limit: int) -> List:
    async with pool.acquire() as con:
        async with con.cursor() as cur:
            await cur.execute(select_gifts, (room_id, start, limit))
            data = await cur.fetchall()
            return [(*item[:-1], str(item[-1])) for item in data]

# -------------------------------------------------------------------------- Query --
