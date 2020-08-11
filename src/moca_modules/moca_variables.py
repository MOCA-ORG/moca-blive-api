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
from multiprocessing import cpu_count, current_process
from socket import gethostname, gethostbyname
from uuid import uuid4
from pytz import timezone
from os import environ
from ujson import loads, dumps
from pathlib import Path
from requests import get, Response, RequestException
from sys import platform, exit

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

if platform == 'win32' or platform == 'cygwin':
    NEW_LINE = '\r\n'
else:
    NEW_LINE = '\n'

# system property
CPU_COUNT: int = cpu_count()
HOST_NAME: str = gethostname()
HOST: str = gethostbyname(HOST_NAME)
PROCESS_ID: Optional[int] = current_process().pid
PROCESS_NAME: str = current_process().name

REQUIREMENTS: Path = Path(__file__).parent.joinpath('requirements.txt')

# THe license of MocaSystem.
LICENSE: str = """
MIT License

Copyright 2020.5.28 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# logo
EL_S: str = """Ω*
              ■          ■■■■■  
              ■         ■■   ■■ 
              ■        ■■     ■ 
              ■        ■■       
    ■■■■■     ■        ■■■      
   ■■   ■■    ■         ■■■     
  ■■     ■■   ■          ■■■■   
  ■■     ■■   ■            ■■■■ 
  ■■■■■■■■■   ■              ■■■
  ■■          ■               ■■
  ■■          ■               ■■
  ■■     ■    ■        ■■     ■■
   ■■   ■■    ■   ■■■  ■■■   ■■ 
    ■■■■■     ■   ■■■    ■■■■■
"""

# japanese Hiragana list
# あ -- ん [:46]
# ぁ -- っ [46:55]
# が -- ぽ [55:]
HIRAGANA: List[str] = ["あ", "い", "う", "え", "お",
                       "か", "き", "く", "け", "こ",
                       "さ", "し", "す", "せ", "そ",
                       "た", "ち", "つ", "て", "と",
                       "な", "に", "ぬ", "ね", "の",
                       "は", "ひ", "ふ", "へ", "ほ",
                       "ま", "み", "む", "め", "も",
                       "や", "ゆ", "よ",
                       "ら", "り", "る", "れ", "ろ",
                       "わ", "を",
                       "ん",
                       "ぁ", "ぃ", "ぅ", "ぇ", "ぉ",
                       "ゃ", "ゅ", "ょ",
                       "っ",
                       "が", "ぎ", "ぐ", "げ", "ご",
                       "ざ", "じ", "ず", "ぜ", "ぞ",
                       "だ", "ぢ", "づ", "で", "ど",
                       "ば", "び", "ぶ", "べ", "ぼ",
                       "ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]

# japanese Katakana list
# ア -- ン [:46]
# ァ -- ッ [46:55]
# ガ -- ポ [55:]
KATAKANA: List[str] = ["ア", "イ", "ウ", "エ", "オ",
                       "カ", "キ", "ク", "ケ", "コ",
                       "サ", "シ", "ス", "セ", "ソ",
                       "タ", "チ", "ツ", "テ", "ト",
                       "ナ", "ニ", "ヌ", "ネ", "ノ",
                       "ハ", "ヒ", "フ", "ヘ", "ホ",
                       "マ", "ミ", "ム", "メ", "モ",
                       "ヤ", "ユ", "ヨ",
                       "ラ", "リ", "ル", "レ", "ロ",
                       "ワ", "ヲ",
                       "ン",
                       "ァ", "ィ", "ゥ", "ェ", "ォ",
                       "ャ", "ュ", "ョ",
                       "ッ",
                       "ガ", "ギ", "グ", "ゲ", "ゴ",
                       "ザ", "ジ", "ズ", "ゼ", "ゾ",
                       "ダ", "ヂ", "ヅ", "デ", "ド",
                       "バ", "ビ", "ブ", "ベ", "ボ",
                       "パ", "ピ", "プ", "ペ", "ポ"]

# alphabet uppercase letter
ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                      'H', 'I', 'J', 'K', 'L', 'M', 'N',
                      'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z']

# alphabet lowercase letter
ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                      'h', 'i', 'j', 'k', 'l', 'm', 'n',
                      'o', 'p', 'q', 'r', 's', 't', 'u',
                      'v', 'w', 'x', 'y', 'z']

# number list
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# chinese number list
CHINESE_DIGITS_COMPLEX = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
CHINESE_DIGITS_SIMPLE = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九']

# japanese number list
JAPANESE_DIGITS_HIRAGANA = ['いち', 'に', 'さん', 'し', 'ご', 'ろく', 'しち', 'はち', 'きゅう', 'じゅう']
JAPANESE_DIGITS_KATAKANA = ['イチ', 'ニ', 'サン', 'シ', 'ゴ', 'ロク', 'シチ', 'ハチ', 'キュウ', 'ジュウ']


class ConsoleColor:
    """
    Color data type
    """
    BLACK: str = '\033[30m'
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    PURPLE: str = '\033[35m'
    CYAN: str = '\033[36m'
    WHITE: str = '\033[37m'
    END: str = '\033[0m'
    BOLD: str = '\038[1m'
    UNDERLINE: str = '\033[4m'
    INVISIBLE: str = '\033[08m'
    REVERCE: str = '\033[07m'


# a random string.
RANDOM_KEY = uuid4().hex + uuid4().hex + uuid4().hex + uuid4().hex

# core.json
core_json: dict
try:
    with open(str(Path(__file__).parent.joinpath('core.json')), 'r', encoding='utf-8') as __core_json_file:
        core_json = loads(__core_json_file.read())
except FileNotFoundError:
    try:
        __response: Response = get('https://www.el-ideal-ideas.com/moca/data/core.json', timeout=5)
        __data = __response.content.decode('utf-8')
        with open(str(Path(__file__).parent.joinpath('core.json')), 'w', encoding='utf-8') as __core_json_file:
            __core_json_file.write(__data)
            core_json = loads(__data)
        del __response, __data
    except RequestException:
        print("Missing core.json file. "
              "can't download core.json from "
              "https://www.el-ideal-ideas.com/moca/data/core.json")
        exit(1)
del __core_json_file

# timezone
TIME_ZONE = environ.get('TIME_ZONE', core_json.get('timezone', 'Asia/Beijing'))
tz = timezone(TIME_ZONE)

# official server
OFFICIAL_SERVER = core_json.get('official_server', 'https://www.el-ideal-ideas.com/')

SELF_IP: str = ''
try:
    __res: Response = get(f'{OFFICIAL_SERVER}moca/apis/ip.php', timeout=5)
    SELF_IP = __res.content.decode('utf-8')
    del __res
except RequestException:
    pass

# private key
SHORT_PRIVATE_KEY: str
if core_json.get('SHORT_PRIVATE_KEY') is None:
    SHORT_PRIVATE_KEY = uuid4().hex[:16]
    core_json['SHORT_PRIVATE_KEY'] = SHORT_PRIVATE_KEY
else:
    SHORT_PRIVATE_KEY = str(core_json.get('SHORT_PRIVATE_KEY'))
    
LONG_PRIVATE_KEY: str
if core_json.get('LONG_PRIVATE_KEY') is None:
    LONG_PRIVATE_KEY = uuid4().hex + uuid4().hex
    core_json['LONG_PRIVATE_KEY'] = LONG_PRIVATE_KEY
else:
    LONG_PRIVATE_KEY = str(core_json.get('LONG_PRIVATE_KEY'))

with open(str(Path(__file__).parent.joinpath('core.json')), 'w', encoding='utf-8') as __core_json_file:
    __core_json_file.write(dumps(core_json, ensure_ascii=False, sort_keys=True, indent=True))
del __core_json_file

# -------------------------------------------------------------------------- Variables --
