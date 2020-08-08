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
from sys import stdout
from traceback import format_exc
from datetime import datetime, date
from .moca_variables import NEW_LINE, tz
from .moca_utils import location
from .moca_base_class import MocaClassCache, MocaNamedInstance
from multiprocessing import current_process
from threading import get_ident
from aiofiles import open as aio_open
from asyncio import get_event_loop

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

# -------------------------------------------------------------------------- Variables --

# -- LogLevel --------------------------------------------------------------------------


class LogLevel(object):
    """The logging level for Moca Log Class."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    @classmethod
    def int_to_str(cls, integer: int) -> str:
        if integer == 0:
            return 'DEBUG'
        elif integer == 1:
            return 'INFO'
        elif integer == 2:
            return 'WARNING'
        elif integer == 3:
            return 'ERROR'
        elif integer == 4:
            return 'CRITICAL'
        else:
            raise ValueError('Invalid integer value, only 0, 1, 2, 3, 4')

    @classmethod
    def str_to_int(cls, string: str) -> int:
        if string == 'DEBUG':
            return 0
        elif string == 'INFO':
            return 1
        elif string == 'WARNING':
            return 2
        elif string == 'ERROR':
            return 3
        elif string == 'CRITICAL':
            return 4
        else:
            raise ValueError('Invalid string value, only DEBUG, INFO, WARNING, ERROR, CRITICAL')

# -------------------------------------------------------------------------- LogLevel --

# -- Moca File Log --------------------------------------------------------------------------


class MocaFileLog(MocaClassCache, MocaNamedInstance):
    """
    Write logs to the log file.

    Attributes
    ----------
    self._filename: Path
        The file path of the log file.
    self._exc_filename: Path
        the file path to save exceptions.
    self._rotate: bool
        rotate the log file or not.
    self._file
        the file object to write logs.
    self._exc_file
        the file object to write exceptions.
    self._level: int
        current logging level.
    self._pid: Optional[int]
        the process id.
    self._last_modified: date
        the last modification date.
    """

    LogLevel = LogLevel

    def __init__(self, filename: Union[str, Path], exc_filename: Union[str, Path], log_rotate: bool = True):
        """
        :param filename: the file path of the log file.
        :param exc_filename: the file path to save exceptions.
        :param log_rotate: rotate the log file automatically.
        """
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        # set log rotation flag
        self._rotate: bool = log_rotate
        # set file path
        self._filename: Path = Path(filename)
        self._exc_filename: Path = Path(exc_filename)
        # set file object
        self._file = open(str(self._filename), mode='a', encoding='utf-8')
        self._exc_file = open(str(self._exc_filename), mode='a', encoding='utf-8')
        # set log level
        self._level: int = LogLevel.INFO
        # set process id
        self._pid: Optional[int] = current_process().pid
        # set last modified time
        self._last_modified: date = datetime.now(tz=tz).date()

    def __del__(self):
        self._file.close()
        self._exc_file.close()

    def __str__(self) -> str:
        return f"MocaFileLog: {self._filename}"

    @property
    def filename(self) -> Path:
        return self._filename

    @property
    def exc_filename(self) -> Path:
        return self._exc_filename

    @property
    def log_rotate(self) -> bool:
        return self._rotate

    @property
    def file(self):
        return self._file

    @property
    def exc_file(self):
        return self._exc_file

    @property
    def level(self) -> int:
        return self._level

    def start_log_rotate(self) -> None:
        """Start the auto-rotation"""
        self._rotate = True

    def stop_log_rotate(self) -> None:
        """Stop the auto-rotation"""
        self._rotate = False

    def set_log_level(self, level: int) -> None:
        """Set the log level."""
        self._level = level
        self.save(f"MocaFileLog: Logging level changed to {LogLevel.int_to_str(level)}!", LogLevel.INFO)

    def save(self, message: str, level: int) -> None:
        """
        Save a log message to the log file.
        :param message: the log message.
        :param level: the log level.
        :return: None
        Log Format
        ----------
        [loglevel](time)<filename|caller|line number|process id|thread id>message
        """
        if level >= self._level:
            filename, caller, line = location()
            current_time = datetime.now(tz=tz)
            current_date = current_time.date()
            if self._rotate and (current_date != self._last_modified):
                self.rotate_log_file()
            self._last_modified = current_date
            msg = f"[{LogLevel.int_to_str(level)}]({str(current_time)})" \
                  f"<{filename}|{caller}|{line}|{self._pid or 0}|{get_ident()}>" \
                  f"{message}"
            print(msg, end=NEW_LINE, file=self._file, flush=True)
            error = format_exc()
            if not error.startswith('NoneType'):
                print(error, end='', file=self._exc_file, flush=True)

    def save_exception(self) -> None:
        """Save the exception traceback information."""
        print(format_exc(), end='', file=self._exc_file, flush=True)

    def start_dev_mode(self) -> None:
        """Show all logs on the console."""
        file = self._file
        exc_file = self._exc_file
        self._file = stdout
        self._exc_file = stdout
        file.close()
        exc_file.close()
        self.save_cache('log_level', self._level)
        self._level = LogLevel.DEBUG
        self.save("MocaFileLog: Development mode started!", LogLevel.INFO)

    def stop_dev_mode(self) -> None:
        """Stop development mode."""
        self.save("MocaFileLog: Development mode stopped!", LogLevel.INFO)
        self._level = self.get_cache('log_level')
        self._file = open(str(self._filename), mode='a', encoding='utf-8')
        self._exc_file = open(str(self._exc_filename), mode='a', encoding='utf-8')

    def get_all_logs(self) -> str:
        """Return today's logs'"""
        with open(str(self._filename), mode='r', encoding='utf-8') as log_file:
            return log_file.read()

    def get_all_logs_as_list(self) -> List[str]:
        """Return a list of today's logs."""
        return self.get_all_logs().splitlines()

    def get_all_exceptions(self) -> str:
        """Return today's exceptions'"""
        with open(str(self._exc_filename), mode='r', encoding='utf-8') as exc_file:
            return exc_file.read()

    def clear_logs(self) -> None:
        """Clear today's logs"""
        self._file.close()
        self._exc_file.close()
        self._filename.unlink()
        self._exc_filename.unlink()
        self._file = open(str(self._filename), mode='a', encoding='utf-8')
        self._exc_file = open(str(self._exc_filename), mode='a', encoding='utf-8')
        self.save("MocaFileLog: Cleared logs!", LogLevel.INFO)

    def rotate_log_file(self) -> None:
        """Rotate the log file."""
        self._file.close()
        self._exc_file.close()
        time = str(datetime.now(tz=tz).date())
        new_filename = self._filename.parent.joinpath(
            f"{'.'.join(self._filename.name.split('.')[:-1])}-{time}.{self._filename.name.split('.')[-1]}"
        )
        new_exc_filename = self._exc_filename.parent.joinpath(
            f"{'.'.join(self._exc_filename.name.split('.')[:-1])}-{time}.{self._exc_filename.name.split('.')[-1]}"
        )
        if new_filename.is_file():
            new_filename.unlink()
        if new_exc_filename.is_file():
            new_exc_filename.unlink()
        self._filename.rename(str(new_filename))
        self._exc_filename.rename(str(new_exc_filename))
        self._file = open(str(self._filename), mode='a', encoding='utf-8')
        self._exc_file = open(str(self._exc_filename), mode='a', encoding='utf-8')

    def get_old_logs(self, year: int, month: int, day: int) -> Optional[str]:
        """Return the old logs as list. If can't found the file, return None."""
        old_filename, _ = self._old_filename(year, month, day)
        if old_filename.is_file():
            with open(str(old_filename), mode='r', encoding='utf-8') as log_file:
                return log_file.read()
        else:
            return None

    def get_old_logs_as_list(self, year: int, month: int, day: int) -> Optional[List[str]]:
        """Return the old logs. If can't found the file, return None."""
        old_logs = self.get_old_logs(year, month, day)
        if old_logs is None:
            return None
        else:
            return old_logs.splitlines()

    def get_old_exceptions(self, year: int, month: int, day: int) -> Optional[str]:
        """Return the old exceptions, If can't found the file, return None."""
        _, old_filename = self._old_filename(year, month, day)
        if old_filename.is_file():
            with open(str(old_filename), mode='r', encoding='utf-8') as log_file:
                return log_file.read()
        else:
            return None

    def _old_filename(self, year: int, month: int, day: int) -> Tuple[Path, Path]:
        """Return the old filename."""
        time = str(datetime(year, month, day).date())
        exc_old_filename = self._exc_filename.parent.joinpath(
            f"{'.'.join(self._exc_filename.name.split('.')[:-1])}-{time}.{self._exc_filename.name.split('.')[-1]}"
        )
        old_filename = self._filename.parent.joinpath(
            f"{'.'.join(self._filename.name.split('.')[:-1])}-{time}.{self._filename.name.split('.')[-1]}"
        )
        return old_filename, exc_old_filename

# -------------------------------------------------------------------------- Moca File Log --

# -- Moca Asynchronous File Log --------------------------------------------------------------------------


class MocaAsyncFileLog(MocaClassCache, MocaNamedInstance):
    """
    Write logs to the log file asynchronously.

    Attributes
    ----------
    self._filename: Path
        The file path of the log file.
    self._exc_filename: Path
        the file path to save exceptions.
    self._rotate: bool
        rotate the log file or not.
    self._file
        the file object to write logs.
    self._exc_file
        the file object to write exceptions.
    self._level: int
        current logging level.
    self._pid: Optional[int]
        the process id.
    self._last_modified: date
        the last modification date.
    self._dev_flag: bool
        the development flag.
    """

    LogLevel = LogLevel

    def __init__(self, filename: Union[str, Path], exc_filename: Union[str, Path], log_rotate: bool = True):
        """
        :param filename: the file path of the log file.
        :param exc_filename: the file path to save exceptions.
        :param log_rotate: rotate the log file automatically.
        """
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        # set log rotation flag
        self._rotate: bool = log_rotate
        # set file path
        self._filename: Path = Path(filename)
        self._exc_filename: Path = Path(exc_filename)
        # set log level
        self._level: int = LogLevel.INFO
        # set process id
        self._pid: Optional[int] = current_process().pid
        # set last modified time
        self._last_modified: date = datetime.now(tz=tz).date()
        # set development flag
        self._dev_flag: bool = False
        # set file object
        self._file = None
        self._exc_file = None

    async def init(self):
        self._file = await aio_open(str(self._filename), mode='a', encoding='utf-8')
        self._exc_file = await aio_open(str(self._exc_filename), mode='a', encoding='utf-8')

    def __del__(self):
        get_event_loop().run_until_complete(self._del())

    async def _del(self):
        await self._file.close()
        await self._exc_file.close()

    def __str__(self) -> str:
        return f"MocaAsyncFileLog: {self._filename}"

    @property
    def filename(self) -> Path:
        return self._filename

    @property
    def exc_filename(self) -> Path:
        return self._exc_filename

    @property
    def log_rotate(self) -> bool:
        return self._rotate

    @property
    def file(self):
        return self._file

    @property
    def exc_file(self):
        return self._exc_file

    @property
    def level(self) -> int:
        return self._level

    def start_log_rotate(self) -> None:
        """Start the auto-rotation"""
        self._rotate = True

    def stop_log_rotate(self) -> None:
        """Stop the auto-rotation"""
        self._rotate = False

    async def set_log_level(self, level: int) -> None:
        """Set the log level."""
        self._level = level
        await self.save(f"MocaAsyncFileLog: Logging level changed to {LogLevel.int_to_str(level)}!", LogLevel.INFO)

    async def save(self, message: str, level: int) -> None:
        """
        Save a log message to the log file.
        :param message: the log message.
        :param level: the log level.
        :return: None
        Log Format
        ----------
        [loglevel](time)<filename|caller|line number|process id|thread id>message
        """
        if level >= self._level:
            filename, caller, line = location()
            current_time = datetime.now(tz=tz)
            current_date = current_time.date()
            if self._rotate and (current_date != self._last_modified):
                await self.rotate_log_file()
            self._last_modified = current_date
            msg = f"[{LogLevel.int_to_str(level)}]({str(current_time)})" \
                  f"<{filename}|{caller}|{line}|{self._pid or 0}|{get_ident()}>" \
                  f"{message}"
            if self._dev_flag:
                print(msg, end=NEW_LINE)
            else:
                await self._file.write(msg)
                await self._file.write(NEW_LINE)
                await self._file.flush()
            error = format_exc()
            if not error.startswith('NoneType'):
                if self._dev_flag:
                    print(error, end='')
                else:
                    await self._exc_file.write(error)
                    await self._exc_file.flush()

    async def save_exception(self) -> None:
        """Save the exception traceback information."""
        if self._dev_flag:
            print(format_exc(), end='')
        else:
            await self._exc_file.write(format_exc())
            await self._exc_file.flush()

    async def start_dev_mode(self) -> None:
        """Show all logs on the console."""
        self.save_cache('log_level', self._level)
        self._level = LogLevel.DEBUG
        self._dev_flag = True
        await self.save("MocaAsyncFileLog: Development mode started!", LogLevel.INFO)

    async def stop_dev_mode(self) -> None:
        """Stop development mode."""
        self._dev_flag = False
        await self.save("MocaAsyncFileLog: Development mode stopped!", LogLevel.INFO)
        self._level = self.get_cache('log_level')

    async def get_all_logs(self) -> str:
        """Return today's logs'"""
        async with aio_open(str(self._filename), mode='r', encoding='utf-8') as log_file:
            return await log_file.read()

    async def get_all_logs_as_list(self) -> List[str]:
        """Return a list of today's logs."""
        logs = await self.get_all_logs()
        return logs.splitlines()

    async def get_all_exceptions(self) -> str:
        """Return today's exceptions'"""
        async with aio_open(str(self._exc_filename), mode='r', encoding='utf-8') as exc_file:
            return await exc_file.read()

    async def clear_logs(self) -> None:
        """Clear today's logs"""
        await self._file.close()
        await self._exc_file.close()
        self._filename.unlink()
        self._exc_filename.unlink()
        await self._init()
        await self.save("MocaAsyncFileLog: Cleared logs!", LogLevel.INFO)

    async def rotate_log_file(self) -> None:
        """Rotate the log file."""
        await self._file.close()
        await self._exc_file.close()
        time = str(datetime.now(tz=tz).date())
        new_filename = self._filename.parent.joinpath(
            f"{'.'.join(self._filename.name.split('.')[:-1])}-{time}.{self._filename.name.split('.')[-1]}"
        )
        new_exc_filename = self._exc_filename.parent.joinpath(
            f"{'.'.join(self._exc_filename.name.split('.')[:-1])}-{time}.{self._exc_filename.name.split('.')[-1]}"
        )
        if new_filename.is_file():
            new_filename.unlink()
        if new_exc_filename.is_file():
            new_exc_filename.unlink()
        self._filename.rename(str(new_filename))
        self._exc_filename.rename(str(new_exc_filename))
        await self._init()

    async def get_old_logs(self, year: int, month: int, day: int) -> Optional[str]:
        """Return the old logs as list. If can't found the file, return None."""
        old_filename, _ = self._old_filename(year, month, day)
        if old_filename.is_file():
            async with aio_open(str(old_filename), mode='r', encoding='utf-8') as log_file:
                return await log_file.read()
        else:
            return None

    async def get_old_logs_as_list(self, year: int, month: int, day: int) -> Optional[List[str]]:
        """Return the old logs. If can't found the file, return None."""
        old_logs = await self.get_old_logs(year, month, day)
        if old_logs is None:
            return None
        else:
            return old_logs.splitlines()

    async def get_old_exceptions(self, year: int, month: int, day: int) -> Optional[str]:
        """Return the old exceptions, If can't found the file, return None."""
        _, old_filename = self._old_filename(year, month, day)
        if old_filename.is_file():
            async with aio_open(str(old_filename), mode='r', encoding='utf-8') as log_file:
                return await log_file.read()
        else:
            return None

    def _old_filename(self, year: int, month: int, day: int) -> Tuple[Path, Path]:
        """Return the old filename."""
        time = str(datetime(year, month, day).date())
        exc_old_filename = self._exc_filename.parent.joinpath(
            f"{'.'.join(self._exc_filename.name.split('.')[:-1])}-{time}.{self._exc_filename.name.split('.')[-1]}"
        )
        old_filename = self._filename.parent.joinpath(
            f"{'.'.join(self._filename.name.split('.')[:-1])}-{time}.{self._filename.name.split('.')[-1]}"
        )
        return old_filename, exc_old_filename

# -------------------------------------------------------------------------- Moca Asynchronous File Log --
