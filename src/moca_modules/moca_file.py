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
from .moca_base_class import MocaClassCache, MocaNamedInstance
from pathlib import Path
from time import sleep
from threading import Thread
from os import stat
from ujson import dumps, loads

# -------------------------------------------------------------------------- Imports --

# -- Moca Synchronized File --------------------------------------------------------------------------


class MocaSynchronizedFile(MocaClassCache, MocaNamedInstance):
    """
    This class will synchronize with the target file.

    Attributes
    ----------
    self._filename: Path
        the path of target file.
    self._interval: float
        the interval to check update.
    self._file_content: str
        the file content.
    self._file_update_time: float
        the last modification time of the target file.
    self._thread: Thread
        a thread used to check file update.
    self._exit_thread: bool
        if this flag is True, the self._thread will stop.
    """

    def __init__(self, filename: Union[str, Path], check_interval: float = 0.1):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        """
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        # set filename
        self._filename: Path = Path(filename)
        # set check interval
        self._interval: float = check_interval
        # save the file content on memory
        self._file_content: str
        try:
            with open(str(self._filename), mode='r', encoding='utf-8') as file:
                self._file_content = file.read()
        except FileNotFoundError:
            with open(str(self._filename), mode='w', encoding='utf-8') as _:
                pass  # create a new file
            self._file_content = ''
        self._file_update_time: float = stat(str(self._filename)).st_mtime
        # exit thread flag
        self._exit_thread: bool = False
        
        # file check loop
        def check_loop(self_: MocaSynchronizedFile):
            while True:
                if self_._exit_thread:  # check exit thread flag
                    break
                self_.reload_file()
                sleep(self_._interval)

        self._thread: Thread = Thread(target=check_loop, args=(self,), daemon=True)
        self._thread.start()

    def __str__(self) -> str:
        return f'MocaSynchronizedFile: {self._filename}'

    def __del__(self):
        self._exit_thread = True
        self._thread.join()

    @property
    def filename(self) -> Path:
        return self._filename

    @property
    def check_interval(self) -> float:
        return self._interval

    @property
    def file_content(self) -> str:
        return self._file_content

    def change_content(self, new_content: str) -> None:
        """Change the content of the file."""
        self._file_content = new_content
        with open(str(self._filename), mode='w', encoding='utf-8') as file:
            file.write(new_content)

    def reload_file(self) -> None:
        """Reload the file manually."""
        time = stat(str(self._filename)).st_mtime
        if time != self._file_update_time:
            with open(str(self._filename), mode='r', encoding='utf-8') as file:
                self._file_content = file.read()
            self._file_update_time = time

# -------------------------------------------------------------------------- Moca Synchronized File --

# -- Moca Synchronized Json File --------------------------------------------------------------------------


class MocaSynchronizedJsonFile(MocaSynchronizedFile):
    """
    This class will synchronize with the target json file.

    Attributes
    ----------
    self._json_update_time: float
        json update time
    self._json
        the json data
    """

    def __init__(self, filename: Union[str, Path], check_interval: float = 0.1):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        """
        super().__init__(filename, check_interval)
        # set update time
        self._json_update_time: float = self._file_update_time
        # set json data
        if self._file_content == '':
            self.change_content('null')
        self._json = loads(self._file_content)

    def __str__(self) -> str:
        return f'MocaSynchronizedJsonFile: {self._filename}'

    @property
    def json(self) -> Any:
        if self._json_update_time != self._file_update_time:
            try:
                self._json = loads(self._file_content)
            except ValueError:
                pass
        self._json_update_time = self._file_update_time
        return self._json

    def change_json(self, data: Any) -> None:
        """Change json data."""
        self.change_content(dumps(data, ensure_ascii=False, sort_keys=True, indent=4))

# -------------------------------------------------------------------------- Moca Synchronized Json File --

# -- Moca Synchronized Json Dictionary --------------------------------------------------------------------------


class MocaSynchronizedJsonDictionary(MocaSynchronizedJsonFile):
    """
    This class will synchronize with the target json dictionary file.
    """

    def __init__(self, filename: Union[str, Path], check_interval: float = 0.1):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        """
        super().__init__(filename, check_interval)
        if not isinstance(self.json, dict):
            self.change_json({})

    def __str__(self) -> str:
        return f'MocaSynchronizedJsonDictionary: {self._filename}'

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key. If can't found the key, return default."""
        return self.json.get(key, default)

    def get_all(self) -> dict:
        return self.json

    def set(self, key: str, value: Any) -> None:
        """Set a value by key."""
        json = self.json
        json[key] = value
        self.change_json(json)

    def remove(self, key: str) -> None:
        """Remove a value by key."""
        json = self.json
        try:
            del json[key]
        except KeyError:
            pass
        self.change_json(json)

    def clear(self) -> None:
        """Clear the dictionary."""
        self.change_json({})

# -------------------------------------------------------------------------- Moca Synchronized Json Dictionary --
