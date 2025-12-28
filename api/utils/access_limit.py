from fastapi import Depends,Request
from redis import asyncio as aioredis
from utils.redis_tools import get_redis
import os,time
from utils.logs import logger

WHITELIST_IPS = os.getenv("WHITELIST_IPS", "").split(",")
ACCESS_LIMIT_PER_DAY = int(os.getenv("ACCESS_LIMIT_PER_DAY", 1))  # 默认值为1

async def check_ip_access(request: Request, redis: aioredis.Redis = Depends(get_redis)):
    
    """检查 IP 访问限制"""
    client_ip = request.headers.get("x-real-ip") or request.client.host
    # print(f"ip: {client_ip}")
    logger.info(f"WHITELIST_IPS: {WHITELIST_IPS}")
    logger.info(f"ip: {client_ip}")
    if client_ip in WHITELIST_IPS:
        return  {
            "status": "success",
            "message": "白名单成员不限制访问",
        }

    redis_key = f"ip_access:{client_ip}:{time.strftime('%Y%m%d')}"
    
    access_count = await redis.get(redis_key)
    # print(f"访问次数{access_count}")
    logger.info(f"访问次数{access_count}")
    if access_count is None:
        access_count = 0
    else:
        access_count = int(access_count)

    if access_count >= ACCESS_LIMIT_PER_DAY:
        print("超过限制次数")
        # 超过限制时返回自定义信息，而不是抛出异常
        return {
            "status": "limited",
            "message": f"AI分析功能每天限制访问{ACCESS_LIMIT_PER_DAY}次,今日访问次数已达上限，请明天再试或联系管理员！",
            "access_count": access_count,
            "limit": ACCESS_LIMIT_PER_DAY
        }

    await redis.incr(redis_key)
    await redis.expire(redis_key, 86400)  # 设置过期时间为一天 (86400 秒)
    return {
        "status": "success"
    }
