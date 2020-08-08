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


# -- Variables --------------------------------------------------------------------------

comments_table = """
create table if not exists comments (
    id bigint auto_increment primary key,
    room_id varchar(32) not null,
    user_name varchar(32) not null,
    comment varchar(128) not null,
    date datetime not null
);
"""

insert_comment = """
insert into comments(room_id, user_name, comment, date)
values(%s, %s, %s, now());
"""

select_comments = """
select * from comments where room_id=%s order by date limit %s, %s;
"""

gifts_table = """
create table if not exists gifts (
    id bigint auto_increment primary key,
    room_id varchar(32) not null,
    user_name varchar(32) not null,
    gift_id varchar(16) not null,
    gift_name varchar(16) not null,
    gift_num varchar(16) not null, 
    coin_type varchar(16) not null,
    total_coin varchar(16) not null,
    date datetime not null
);
"""

insert_gift = """
insert into gifts(room_id, user_name, gift_id, gift_name, gift_num, coin_type, total_coin, date)
values(%s, %s, %s, %s, %s, %s, %s, now())
"""

select_gifts = """
select * from gifts where room_id=%s order by date limit %s, %s;
"""

# -------------------------------------------------------------------------- Variables --
