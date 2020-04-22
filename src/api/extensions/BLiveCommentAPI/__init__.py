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

from .... import core
from ....mysql import mysql_con
from pymysql import Warning
from warnings import filterwarnings
from asyncio import get_event_loop
from .routes import blive
from ...app import app
from uuid import uuid4

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

app.blueprint(blive)

filterwarnings("error", category=Warning)

core.config.get('blive_comment_api_save_gifts', bool, False)
core.config.get('blive_comment_api_save_comments', bool, False)
core.config.get('blive_comment_api_save_raw_data', bool, False)
core.config.get('blive_comment_api_secret_key', str, uuid4().hex)

_gifts_table = """
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

_comments_table = """
create table if not exists user_comments (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    user_name varchar(64) not null,
    comment varchar(128) not null 
); 
"""

_raw_table = """
create table if not exists raw_data (
    id bigint auto_increment primary key,
    room_id varchar(64) not null,
    data TEXT not null
); 
"""

if mysql_con is not None:
    cursor = mysql_con.cursor()
    try:
        cursor.execute(_gifts_table)
    except Warning:
        pass
    try:
        cursor.execute(_comments_table)
    except Warning:
        pass
    try:
        cursor.execute(_raw_table)
    except Warning:
        pass
    try:
        mysql_con.commit()
    except Warning:
        pass

# -------------------------------------------------------------------------- Init --

# -- Log --------------------------------------------------------------------------

get_event_loop().run_until_complete(core.logger.save("Loaded BLiveCommentAPI module successfully.", core.logger.DEBUG))

# -------------------------------------------------------------------------- Log --
