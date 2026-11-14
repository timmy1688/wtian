"""
运营计数的读写。键按上海时间的日期分开，形如 ops:2026-11-14，保留二百天。

一个键里只放次数。不写生辰、问题、卦爻或解读。
Redis 暂时连不上时，计数失败只记日志，不影响排盘和解读。
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from utils.logs import logger

from .huizong import JICHU_ZI, huizong, ye_mian_ziduan

SHANGHAI = ZoneInfo("Asia/Shanghai")
BAOLIU_TIAN = 200


def shanghai_today(now=None):
    """现在的上海日期。传入的时间可以带任意时区。"""
    dangqian = now or datetime.now(SHANGHAI)
    if dangqian.tzinfo is None:
        dangqian = dangqian.replace(tzinfo=SHANGHAI)
    return dangqian.astimezone(SHANGHAI).date()


def _jian(day) -> str:
    return f"ops:{day.isoformat()}"


async def jia(redis, field: str, now=None) -> None:
    if field not in JICHU_ZI:
        raise ValueError(field)
    day = shanghai_today(now)
    key = _jian(day)
    await redis.hincrby(key, field, 1)
    await redis.expire(key, BAOLIU_TIAN * 86400)


async def ji(field: str) -> None:
    """给今天的某一项加一。失败时吞掉异常。"""
    try:
        from utils.redis_tools import get_redis
        await jia(await get_redis(), field)
    except Exception:
        logger.exception("ops count failed field=%s", field)


async def du_qu(redis, today) -> dict:
    """读出保留期内每一天的原始计数。没有键的日子不放进结果。"""
    days = [today - timedelta(days=i) for i in range(BAOLIU_TIAN)]
    pipe = redis.pipeline()
    for day in days:
        pipe.hgetall(_jian(day))
    found = await pipe.execute()
    store = {}
    for day, raw in zip(days, found):
        if raw:
            store[day.isoformat()] = raw
    return store


async def qu_huizong(redis, now=None) -> dict:
    today = shanghai_today(now)
    return huizong(await du_qu(redis, today), today)


__all__ = ["ji", "jia", "qu_huizong", "shanghai_today", "ye_mian_ziduan"]
