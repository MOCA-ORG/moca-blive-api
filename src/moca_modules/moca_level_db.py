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
from .moca_base_class import MocaClassCache, MocaNamedInstance
from pathlib import Path
from dill import dumps, loads

# -------------------------------------------------------------------------- Imports --

# -- Moca Level DB --------------------------------------------------------------------------


class MocaLevelDB(MocaClassCache, MocaNamedInstance):
    """
    Level DB.

    Attributes
    ----------
    self._db: LevelDB
        the level db.
    """

    def __init__(self, db: Union[Path, str]):
        """
        :param db: the filename of level database.
        """
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        self._db: LevelDB = LevelDB(str(db))

    @property
    def db(self) -> LevelDB:
        return self._db

    def put(self, key: bytes, value: Any) -> bool:
        """Add a data to core database."""
        try:
            self._db.Put(key, dumps(value))
            return True
        except (LevelDBError, ValueError, TypeError):
            return False

    def get(self, key: bytes, default: Any = None) -> Any:
        """Get a data from core database."""
        try:
            return loads(self._db.Get(key))
        except (LevelDBError, ValueError, TypeError, KeyError):
            return default

    def delete(self, key: bytes) -> bool:
        """Delete data from core database."""
        try:
            self._db.Delete(key)
            return True
        except LevelDBError:
            return False

# -------------------------------------------------------------------------- Moca Level DB --
