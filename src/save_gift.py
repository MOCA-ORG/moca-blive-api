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

from .core import moca_config
from asyncio import run
from .mysql import get_aio_con_with_default_config

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('save_gifts', bool, False)

# -------------------------------------------------------------------------- Init --

# -- Variables --------------------------------------------------------------------------

gifts_table = """
create table if not exists user_gifts (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    user_name varchar(64) not null,
    gift_id varchar(16) not null,
    gift_name varchar(16) not null,
    gift_num varchar(16) not null, 
    coin_type varchar(16) not null,
    total_coin varchar(16) not null
); 
"""

insert_gift = """
insert into user_gifts(room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin) 
values(%s, %s, %s, %s, %s, %s, %s);
"""

# -------------------------------------------------------------------------- Variables --

# -- Setup --------------------------------------------------------------------------

if moca_config.get('save_gifts', bool, False):
    connection = run(get_aio_con_with_default_config())

    async def __execute(query: str):
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            await connection.commit()

    run(__execute(gifts_table))

else:
    connection = None

# -------------------------------------------------------------------------- Setup --

# -- Save Gifts --------------------------------------------------------------------------


async def save_gift(room_id: int, user_name: str, gift_id: str, gift_name: str,
                    gift_num: str, coin_type: str, total_coin: str):
    if moca_config.get('save_gifts', bool, False) and connection is not None:
        async with connection as cursor:
            await cursor.execute(insert_gift, (room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin))
            await connection.commit()

# -------------------------------------------------------------------------- Save Gifts --
