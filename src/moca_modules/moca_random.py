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
from random import choice
from Crypto import Random
from .moca_variables import DIGITS, HIRAGANA, KATAKANA, CHINESE_DIGITS_SIMPLE, CHINESE_DIGITS_COMPLEX

# -------------------------------------------------------------------------- Imports --

# -- Random --------------------------------------------------------------------------


def get_random_bytes(length: int) -> bytes:
    """Get random bytes."""
    return Random.get_random_bytes(length)


def get_random_string(length: int,
                      characters: Optional[Sequence] = None) -> str:
    """
    Create a random string by characters.
    If characters is None create random string use uuid4.
    """
    if characters is None:
        return ''.join([uuid4().hex for _ in range((length // 32) + 1)])[0:length]
    else:
        return ''.join([str(choice(characters)) for _ in range(length)])


def get_random_string_by_digits(length: int) -> str:
    """Create a random string use digits."""
    return get_random_string(length, DIGITS)


def get_random_string_by_hiragana(length: int) -> str:
    """Create a random string use japanese hiragana."""
    return get_random_string(length, HIRAGANA)


def get_random_string_by_katakana(length: int) -> str:
    """Create a random string use japanese katakana."""
    return get_random_string(length, KATAKANA)


def get_random_string_by_kana(length: int) -> str:
    """Create a random string use japanese kana."""
    return get_random_string(length, KATAKANA + HIRAGANA)


def get_a_random_hiragana() -> str:
    """Get one random hiragana character."""
    return choice(HIRAGANA)


def get_a_random_katakana() -> str:
    """Get one random katakana character."""
    return choice(KATAKANA)


def get_a_random_kana() -> str:
    """Get one random hiragana character."""
    return choice(KATAKANA + HIRAGANA)


def get_a_random_chinese_digit_simple() -> str:
    """Get one random chinese digit (simple)."""
    return choice(CHINESE_DIGITS_SIMPLE)


def get_a_random_chinese_digit_complex() -> str:
    """Get one random chinese digit (complex)."""
    return choice(CHINESE_DIGITS_COMPLEX)

# -------------------------------------------------------------------------- Random --
