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
from pathlib import Path
from .moca_file import MocaSynchronizedJsonDictionary

# -------------------------------------------------------------------------- Imports --

# -- Moca File Config --------------------------------------------------------------------------


class MocaFileConfig(MocaSynchronizedJsonDictionary):
    """
    A json file based config manager.
    """

    def __init__(self, filename: Union[str, Path], check_interval: float = 0.1):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        """
        super().__init__(filename, check_interval)

    def get_config(self, key: str, res_type: Any = any, default: Any = None) -> Any:
        """
        Get a config value by key.
        :param key: the config key.
        :param res_type: if res_type is not any, this function will check the response type.
        :param default: return default when can't find the config,
                        or the config is None, or the response type is invalid.
        """
        res = self.get(key)
        if (res is None) or (not isinstance(res, res_type)):
            return default
        else:
            return res

    def get_all_configs(self) -> Any:
        """Get all config values."""
        return self.json

    def set_config(self, key: str, value: Any) -> None:
        """Set a config value."""
        self.set(key, value)

    def remove_config(self, key: str) -> None:
        """Remove a config value."""
        self.remove(key)

    def set_if_not_exists(self, key: str, value: Any) -> None:
        """Set a config value, if it doesn't exist, or it is None."""
        if self.get(key) is None:
            self.set(key, value)

    def get_and_remove(self, key: str, res_type: Any = any, default: Any = None) -> Any:
        """
        Get a config value, and remove it.
        :param key: the config key.
        :param res_type: if res_type is not any, this function will check the response type.
        :param default: return default when can't find the config,
                        or the config is None, or the response type is invalid.
        """
        res = self.get_config(key, res_type, default)
        self.remove_config(key)
        return res

    def remove_all_configs(self) -> None:
        """Remove all configs."""
        self.clear()

# -------------------------------------------------------------------------- Moca File Config --
