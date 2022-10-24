from os import environ
from typing import *

import aiohttp
from async_lru import alru_cache

LRU_CACHE_MAX_SIZE: int = int(environ.get('LRU_CACHE_MAX_SIZE', 1024))
GET_LIVE_INFO_API: str = 'https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s'
GET_USER_INFO_API: str = 'https://api.bilibili.com/x/space/acc/info?mid=%s'

headers: Dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/102.0.0.0 Safari/537.36'
}


@alru_cache(maxsize=LRU_CACHE_MAX_SIZE)
async def get_live_info(room_id: str) -> Optional[dict]:
    """
    获取直播间信息
    :param room_id: 直播间号
    :return: 直播间信息
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(GET_LIVE_INFO_API % room_id) as res:
            if res.status != 200:
                return None
            return await res.json()


async def get_live_status(room_id: str) -> Optional[int]:
    """
    获取直播状态

    :param room_id: 直播间号
    :return: 直播状态

    0：未开播
    1：直播中
    2：轮播中
    """
    info: Optional[dict] = await get_live_info(room_id)
    if info is None:
        return info
    return info['data']['live_status']


@alru_cache(maxsize=LRU_CACHE_MAX_SIZE)
async def get_user_info(user_id: str) -> Optional[dict]:
    """
    获取用户信息

    :param user_id: 用户ID
    :return: 用户信息
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(GET_USER_INFO_API % user_id) as res:
            if res.status != 200:
                return None
            return await res.json()


async def get_user_icon(user_id: str) -> Optional[str]:
    """
    获取用户头像

    :param user_id: 用户ID
    :return: 用户头像URL
    """
    info: Optional[dict] = await get_user_info(user_id)
    if info is None:
        return info
    return info['data']['face']


async def get_user_name(user_id: str) -> Optional[str]:
    """
    获取用户昵称

    :param user_id: 用户ID
    :return: 用户昵称
    """
    info: Optional[dict] = await get_user_info(user_id)
    if info is None:
        return info
    return info['data']['name']
