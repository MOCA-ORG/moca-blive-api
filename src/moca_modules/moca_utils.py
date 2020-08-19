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
from inspect import currentframe, types, stack
from os.path import basename
from pathlib import Path
from sys import executable, platform
from subprocess import call
from .moca_variables import LICENSE, NEW_LINE, tz, ConsoleColor, HIRAGANA, KATAKANA, core_json, PROCESS_ID
from git.repo.base import Repo
from random import randint
from time import time
from requests import get, Response
from hashlib import md5, sha1, sha256, sha512, sha224, sha384
from datetime import datetime
from time import sleep
from threading import Thread
from multiprocessing import Process
from json import dump, dumps
from io import StringIO
from uuid import uuid4
from re import compile
from pickle import dumps as p_dumps, loads as p_loads
from gzip import compress, decompress
from multiprocessing import current_process
from setproctitle import setproctitle
from html import escape, unescape

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

email_pattern = compile('^[0-9a-z_./?-]+@([0-9a-z-]+.)+[0-9a-z-]+$')

# -------------------------------------------------------------------------- Variables --

# -- Utilities --------------------------------------------------------------------------


def location() -> Tuple[str, str, int]:
    """
    :return: filename, caller name, line number
    """
    frame: Optional[types.FrameType] = currentframe()
    if frame is None:
        return 'unknown', 'unknown', -1
    else:
        return basename(frame.f_back.f_back.f_code.co_filename), \
               frame.f_back.f_back.f_code.co_name, \
               frame.f_back.f_back.f_lineno


def caller_name() -> str:
    """Return caller name."""
    frame: Optional[types.FrameType] = currentframe()
    if frame is None:
        return 'unknown'
    else:
        return frame.f_back.f_back.f_code.co_name


def self_name() -> str:
    """Return self name."""
    try:
        return stack()[1][3]
    except IndexError:
        return 'unknown'


def print_debug(msg: str) -> None:
    print('[DEBUG] ' + msg)


def print_info(msg: str) -> None:
    print('\033[32m' + '[INFO] ' + msg + '\033[0m')


def print_warning(msg: str) -> None:
    print('\033[33m' + '[WARNING] ' + msg + '\033[0m')


def print_error(msg: str) -> None:
    print('\033[31m' + '[ERROR] ' + msg + '\033[0m')


def print_critical(msg: str) -> None:
    print('\033[31m' + '[CRITICAL] ' + msg + '\033[0m')


def print_license() -> None:
    """Print license to console."""
    print(LICENSE)


def save_license_to_file(filename: Union[str, Path]) -> None:
    """Save the license to the file."""
    with open(str(filename), 'w') as file:
        print(LICENSE, end=NEW_LINE, file=file)


def install_modules(module: Union[str, List[str]]) -> None:
    """Install a python module use pip."""
    if platform == 'win32' or platform == 'cygwin':
        call(
            f"{executable} -m pip install {module if isinstance(module, str) else ' '.join(module)}"
            f" --upgrade --no-cache-dir > nul",
            shell=True
        )
    else:
        call(
            f"{executable} -m pip install {module if isinstance(module, str) else ' '.join(module)}"
            f" --upgrade --no-cache-dir > /dev/null",
            shell=True
        )


def install_requirements_file(filename: Union[str, Path]) -> None:
    """Install a python module use pip."""
    if platform == 'win32' or platform == 'cygwin':
        call(
            f"{executable} -m pip install -r {str(filename)}"
            f" --upgrade --no-cache-dir > nul",
            shell=True
        )
    else:
        call(
            f"{executable} -m pip install -r {str(filename)}"
            f" --upgrade --no-cache-dir > /dev/null",
            shell=True
        )


def git_clone(url: str, path: Union[Path, str]) -> None:
    """Clone a git repository."""
    Repo.clone_from(url, str(path))


def wget(url: str, filename: Union[Path, str]) -> bool:
    """
    Download a file from url.
    if the http status code is 200 return true.
    """
    res: Response = get(url, allow_redirects=True)
    if res.status_code == 200:
        with open(str(filename), mode='wb') as file:
            file.write(res.content)
        return True
    else:
        return False


def wcheck(url: str) -> bool:
    """If the http status is 200 return true."""
    res: Response = get(url, allow_redirects=True)
    return res.status_code == 200


def wstatus(url: str) -> int:
    """return the http status code."""
    res: Response = get(url, allow_redirects=True)
    return res.status_code


def disk_speed(path: Union[str, Path]) -> Tuple[float, float]:
    """return read(MB/s), write(MB/s)"""
    if Path(path).is_dir():
        filename = Path(path).joinpath('tmp.data')
    else:
        filename = Path(path)
    cluster_size = 64 * 1024
    file_size = 1000 * 1024 * 1024

    def calculate_results(start: float, end: float):
        diff = end - start
        speed = file_size / diff / 1024 / 1024
        return round(speed, 2)

    current = 0
    data = ""
    for i in range(cluster_size):
        data += str(randint(0, 1))
    start_write = time()
    file = open(str(filename), "wb")
    while current <= file_size:
        file.write(data.encode())
        current += cluster_size
    file.close()
    end_write = time()
    current = 0
    start_read = time()
    file = open(str(filename), "rb")
    while current <= file_size:
        file.read(cluster_size)
        current += cluster_size
    file.close()
    end_read = time()
    res_read = calculate_results(start_read, end_read)
    res_write = calculate_results(start_write, end_write)
    try:
        filename.unlink()
    except FileNotFoundError:
        pass
    return res_read, res_write


def check_hash(filename: Union[str, Path], algorithm: str) -> str:
    """
    Return the hash as a string.
    :param filename: the path to the file.
    :param algorithm: (md5, sha1, sha224, sha256, sha384, sha512)
    :return: the hash of the target file.
    """
    if 'md5' == algorithm:
        hash_ = md5()
    elif 'sha224' == algorithm:
        hash_ = sha224()
    elif 'sha256' == algorithm:
        hash_ = sha256()
    elif 'sha384' == algorithm:
        hash_ = sha384()
    elif 'sha512' == algorithm:
        hash_ = sha512()
    else:
        hash_ = sha1()

    with open(str(filename), mode='rb') as f:
        while True:
            chunk = f.read(2048 * hash_.block_size)
            if len(chunk) == 0:
                break
            hash_.update(chunk)

    digest = hash_.hexdigest()
    return digest


def get_time_string(only_date: bool = False) -> str:
    """
    Return current time as string.
    example
        only_date == True
            '2019-11-08'
        only_date == False
            '2019-11-08 15:12:16.036244'
    :return: time string.
    """
    if only_date:
        return str(datetime.now(tz).date())
    else:
        return str(datetime.now(tz))


def print_with_color(msg: str,
                     color: str) -> None:
    """
    print message to console with color.
    :param msg: message.
    :param color: color, can use data type ConsoleColor.
    :return: None.
    """
    print(color + msg + ConsoleColor.END)


def add_extension(filename: Union[Path, str],
                  extension: str) -> str:
    """
    Adds an extension to filename.
    :param filename: original filename.
    :param extension: extension to add.
    """
    # set name
    name: str = str(filename)
    # set extension
    if extension.startswith('.'):
        ext = extension
    else:
        ext = '.' + extension
    if name.endswith(ext):  # check name
        return name
    else:
        return name + ext


def add_dot_jpg(filename: Union[Path, str]) -> str:
    """Adds a .jpg extension to filename."""
    return add_extension(filename, '.jpg')


def add_dot_jpeg(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.jpeg')


def add_dot_gif(filename: Union[Path, str]) -> str:
    """Adds a .gif extension to filename."""
    return add_extension(filename, '.gif')


def add_dot_txt(filename: Union[Path, str]) -> str:
    """Adds a .txt extension to filename."""
    return add_extension(filename, '.txt')


def add_dot_png(filename: Union[Path, str]) -> str:
    """Adds a .png extension to filename."""
    return add_extension(filename, '.png')


def add_dot_csv(filename: Union[Path, str]) -> str:
    """Adds a .csv extension to filename."""
    return add_extension(filename, '.csv')


def add_dot_rtf(filename: Union[Path, str]) -> str:
    """Adds a .rtf extension to filename."""
    return add_extension(filename, '.rtf')


def add_dot_pdf(filename: Union[Path, str]) -> str:
    """Adds a .pdf extension to filename."""
    return add_extension(filename, '.pdf')


def add_dot_md(filename: Union[Path, str]) -> str:
    """Adds a .md extension to filename."""
    return add_extension(filename, '.md')


def add_dot_log(filename: Union[Path, str]) -> str:
    """Adds a .log extension to filename."""
    return add_extension(filename, '.log')


def add_dot_json(filename: Union[Path, str]) -> str:
    """Adds a .json extension to filename."""
    return add_extension(filename, '.json')


def add_dot_py(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.py')


def add_dot_cache(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.cache')


def add_dot_pickle(filename: Union[Path, str]) -> str:
    """Adds a .pickle extension to filename."""
    return add_extension(filename, '.pickle')


def add_dot_js(filename: Union[Path, str]) -> str:
    """Adds a .js extension to filename."""
    return add_extension(filename, '.js')


def add_dot_css(filename: Union[Path, str]) -> str:
    """Adds a .css extension to filename."""
    return add_extension(filename, '.css')


def add_dot_html(filename: Union[Path, str]) -> str:
    """Adds a .html extension to filename."""
    return add_extension(filename, '.html')


def set_interval(function: Callable,
                 interval: float,
                 count: Optional[int] = None,
                 other_thread: bool = True) -> None:
    """
    Run function (count) times with interval(seconds).
    :param function: target function.
    :param interval: run function interval.
    :param count: run limit. if this value is None, run function without limit.
    :param other_thread: run on other thread.
    :return: None.
    """
    def __inner_wrapper() -> None:
        remaining = count
        while True:
            if (remaining is None) or (remaining > 0):
                if isinstance(remaining, int):
                    remaining -= 1
                sleep(interval)
                function()
            else:
                break
    if other_thread:
        thread = Thread(target=__inner_wrapper, daemon=True)
        thread.start()
    else:
        __inner_wrapper()


def set_timeout(function: Callable,
                timeout: float,
                other_thread: bool = True) -> None:
    """
    Run function with timeout (seconds).
    :param function: target function.
    :param timeout: timeout (seconds).
    :param other_thread: run on other thread.
    :return: None.
    """
    set_interval(function, timeout, count=1, other_thread=other_thread)


def on_other_thread(func):
    """This is a decorator, can run function on other thread."""
    def decorator(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return decorator


def on_other_process(func):
    """This is a decorator, can run function on other process."""
    def decorator(*args, **kwargs):
        process = Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return decorator


def is_hiragana(text: str) -> bool:
    """Check is text made of hiragana"""
    for character in text:
        if character not in HIRAGANA:
            return False
    return True


def is_small_hiragana(text: str) -> bool:
    """Check is text made of small hiragana"""
    small_hiragana = HIRAGANA[46:55]
    for character in text:
        if character not in small_hiragana:
            return False
    return True


def is_katakana(text: str) -> bool:
    """Check is text made of katakana"""
    for character in text:
        if character not in KATAKANA:
            return False
    return True


def is_small_katakana(text: str) -> bool:
    """Check is text made of small katakana"""
    small_katakana = KATAKANA[46:55]
    for character in text:
        if character not in small_katakana:
            return False
    return True


def hiragana_to_katakana(hiragana: str,
                         hide_other: bool = False) -> str:
    """Convert hiragana characters to katakana characters"""
    if hide_other:
        return ''.join([KATAKANA[HIRAGANA.index(character)] if character in HIRAGANA else
                        character if character in KATAKANA else
                        '' for character in hiragana])
    else:
        return ''.join([KATAKANA[HIRAGANA.index(character)] if character in HIRAGANA else
                        character for character in hiragana])


def katakana_to_hiragana(katakana: str,
                         hide_other: bool = False) -> str:
    """Convert katakana characters to hiragana characters"""
    if hide_other:
        return ''.join([HIRAGANA[KATAKANA.index(character)] if character in KATAKANA else
                        character if character in HIRAGANA else
                        '' for character in katakana])
    else:
        return ''.join([HIRAGANA[KATAKANA.index(character)] if character in KATAKANA else
                        character for character in katakana])


def check_length(min_length: int,
                 max_length: int,
                 mode: str = 'and',
                 *args) -> bool:
    """
    check items length is between min_length and max_length
    :param min_length: minimum length
    :param max_length: maximum length
    :param mode: check mode, 'and': all items need clear length check, 'or': more than one item need clear length check
    :param args: items
    :return: status, [correct] or [incorrect]
    """
    if mode == 'and':
        for item in args:
            if not (min_length <= len(item) <= max_length):
                return False  # if found incorrect item, stop check-loop and return False
        return True  # if can't found incorrect item, return True
    else:
        for item in args:
            if min_length <= len(item) <= max_length:
                return True  # if found correct item, stop check-loop and return True
        return False  # if can't found correct item, return False


def dump_json_beautiful(data: Any,
                        file: Union[StringIO, Path, str]) -> None:
    """Dump json data to file with beautiful format."""
    if isinstance(file, StringIO):
        dump(data, file, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    else:
        if isinstance(file, Path):
            path = file
        else:
            path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(file), mode='w', encoding='utf-8') as output_file:
            dump(data, output_file, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def dumps_json_beautiful(data: Any) -> str:
    """Dump json data as string with beautiful format."""
    return dumps(data, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def contains_upper(text: str) -> bool:
    """If text contains upper case characters, return True."""
    for character in text:
        if character.isupper():
            return True
    return False


def contains_lower(text: str) -> bool:
    """If text contains lower case characters, return True."""
    for character in text:
        if character.islower():
            return True
    return False


def contains_alpha(text: str) -> bool:
    """If text contains alphabet, return True."""
    for character in text:
        if character.isalpha():
            return True
    return False


def contains_digit(text: str) -> bool:
    """If text contains a digit, return True."""
    for character in text:
        if character.isdigit():
            return True
    return False


def contains_symbol(text: str, symbols: Optional[str] = None) -> bool:
    """If text contains a symbol in symbols, return True."""
    if symbols is None:
        for character in text:
            if character.isascii() and (not character.isalnum()):
                return True
        return False
    else:
        for character in text:
            if character in symbols:
                return True
        return False


def only_consist_of(target: Union[str, List[str]], characters: Union[str, List[str]],) -> bool:
    """If 'target' only contains of 'characters' return True"""
    for character in target:
        if character not in characters:
            return False
    return True


def reset_private_key() -> None:
    """Reset private key."""
    core_json['SHORT_PRIVATE_KEY'] = uuid4().hex[:16]
    core_json['LONG_PRIVATE_KEY'] = uuid4().hex + uuid4().hex
    with open(str(Path(__file__).parent.joinpath('core.json')), 'w', encoding='utf-8') as __core_json_file:
        __core_json_file.write(dumps(core_json, ensure_ascii=False, sort_keys=True, indent=True))
    print_info('core.json was changed, please restart system.')


def to_hankaku(text: str) -> str:
    """半角変換"""
    return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))


def to_zenkaku(text: str) -> str:
    """全角変換"""
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


def check_email_format(email: str) -> bool:
    return email_pattern.match(email) is not None


def moca_dumps(obj: Any) -> bytes:
    """serialize and compress."""
    data = p_dumps(obj)
    if len(data) > 1024:
        return b'moca' + compress(data)
    else:
        return data


def moca_loads(data: Optional[bytes]) -> Any:
    """Load serialized object."""
    if data is None:
        return None
    elif data[:4] == b'moca':
        return p_loads(decompress(data[4:]))
    else:
        return p_loads(data)


def print_only_in_main_process(*args, sep=' ', end='\n', file=None) -> None:
    if current_process().pid == PROCESS_ID:
        print(*args, sep=sep, end=end, file=file)


def set_process_name(name: str) -> None:
    setproctitle(name)


def html_escape(text: str) -> str:
    return escape(text)


def html_unescape(text: str) -> str:
    return unescape(text)


def word_block(text: str, blocked_words: List[str], replace: str = '****') -> str:
    tmp_string: str = text
    for word in blocked_words:
        if word in tmp_string:
            tmp_string = tmp_string.replace(word, replace)
    return tmp_string

# -------------------------------------------------------------------------- Utilities --
