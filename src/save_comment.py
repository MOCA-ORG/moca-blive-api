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

from .core import moca_config, loop
from .mysql import get_aio_con_with_default_config
from warnings import filterwarnings
from pymysql import Warning

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

moca_config.get('save_comments', bool, False)

filterwarnings("error", category=Warning)

# -------------------------------------------------------------------------- Init --

# -- Variables --------------------------------------------------------------------------

comments_table = """
create table if not exists user_comments (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    user_name varchar(64) not null,
    comment varchar(128) not null 
); 
"""

insert_comment = """
insert into user_comments(room_id, user_name, comment) 
values(%s, %s, %s);
"""

# -------------------------------------------------------------------------- Variables --

# -- Setup --------------------------------------------------------------------------

if moca_config.get('save_comments', bool, False):
    connection = loop.run_until_complete(get_aio_con_with_default_config())

    async def __execute(query: str):
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            await connection.commit()

    loop.run_until_complete(__execute(comments_table))

else:
    connection = None

# -------------------------------------------------------------------------- Setup --

# -- Save Comments --------------------------------------------------------------------------


async def save_comment(room_id: int, user_name: str, comment: str):
    if moca_config.get('save_comments', bool, False) and connection is not None:
        async with connection.cursor() as cursor:
            await cursor.execute(insert_comment, (str(room_id), str(user_name), str(comment)))
            await connection.commit()

# -------------------------------------------------------------------------- Save Comments --
