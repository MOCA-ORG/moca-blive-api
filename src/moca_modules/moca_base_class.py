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
from uuid import uuid4

# -------------------------------------------------------------------------- Imports --

# -- Class Cache --------------------------------------------------------------------------


class MocaClassCache(object):
    """
    Can save any data in the class.

    Attributes
    ----------
    self._moca_class_cache_prefix: str
        the prefix of the cache.
    """

    _MOCA_CLASS_CACHE: dict = {}

    def __init__(self):
        self._moca_class_cache_prefix: str = uuid4().hex
        self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix] = {}

    def __del__(self):
        try:
            del self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix]
        except KeyError:
            pass

    def save_cache(self, key: str, value: Any) -> None:
        """Cache a value by key."""
        self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix][key] = value

    def get_cache(self, key: str) -> Any:
        """Get a cached value by key."""
        return self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix].get(key)

    def clear_cache(self) -> None:
        """Clear all cache of this instance."""
        self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix] = {}

    def get_all_cache_of_this_instance(self) -> dict:
        """Get all cache of this instance"""
        return self.__class__._MOCA_CLASS_CACHE[self._moca_class_cache_prefix]

    @classmethod
    def get_all_cache_of_this_class(cls) -> dict:
        """Get all cache of this class."""
        return cls._MOCA_CLASS_CACHE

# -------------------------------------------------------------------------- Class Cache --

# -- Named Instances --------------------------------------------------------------------------


class MocaNamedInstance(object):
    """
    Save all instances and manage by name.

    Attributes
    ----------
    self._instance_name: str
        the name of this instance
    """

    _MOCA_INSTANCE_LIST: dict = {}

    def __init__(self, name: str = None):
        """
        :param name: the name of the instance.
        """
        instance_name = name if name is not None else uuid4().hex
        self.__class__._MOCA_INSTANCE_LIST[instance_name] = self
        self._instance_name: str = instance_name

    def __del__(self):
        try:
            del self.__class__._MOCA_INSTANCE_LIST[self._instance_name]
        except KeyError:
            pass

    @classmethod
    def get_instance(cls, name: str):
        """Get an instance by name."""
        return cls._MOCA_INSTANCE_LIST.get(name)

    @classmethod
    def get_all_instances(cls) -> dict:
        """Get all instances as a dictionary."""
        return cls._MOCA_INSTANCE_LIST

# -------------------------------------------------------------------------- Named Instances --
