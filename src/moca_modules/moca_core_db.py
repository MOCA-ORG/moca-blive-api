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
from leveldb import LevelDB, LevelDBError
from pathlib import Path
from pickle import dumps, loads
from .moca_utils import print_warning
from tinydb import TinyDB, JSONStorage, Query
from tinydb.middlewares import CachingMiddleware

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

try:
    __core_db = LevelDB(str(Path(__file__).parent.joinpath('storage').joinpath('core.db')))
except LevelDBError:
    __core_db = None

core_tiny_db: TinyDB = TinyDB(
    str(Path(__file__).parent.joinpath('storage').joinpath('core-tiny-db.json')),
    CachingMiddleware(JSONStorage),
)
core_tiny_query: Query = Query()

# -------------------------------------------------------------------------- Variables --

# -- Core DB --------------------------------------------------------------------------

if __core_db is None:

    def put(key: bytes, value: Any) -> bool:
        print_warning("Before use moca-core-db, Please stop all system that loaded moca_modules.")
        return False

    def get(key: bytes, default: Any = None) -> Any:
        print_warning("Before use moca-core-db, Please stop all system that loaded moca_modules.")
        return None

    def delete(key: bytes) -> bool:
        print_warning("Before use moca-core-db, Please stop all system that loaded moca_modules.")
        return False
else:

    def put(key: bytes, value: Any) -> bool:
        """Add a data to core database."""
        try:
            __core_db.Put(key, dumps(value))
            return True
        except (LevelDBError, ValueError, TypeError):
            return False


    def get(key: bytes, default: Any = None) -> Any:
        """Get a data from core database."""
        try:
            return loads(__core_db.Get(key))
        except (LevelDBError, ValueError, TypeError, KeyError):
            return default


    def delete(key: bytes) -> bool:
        """Delete data from core database."""
        try:
            __core_db.Delete(key)
            return True
        except LevelDBError:
            return False

# -------------------------------------------------------------------------- Core DB --
