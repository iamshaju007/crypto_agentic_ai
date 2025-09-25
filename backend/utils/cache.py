from redis.asyncio import Redis
from utils.config import get_config

async def get_redis():
    redis = Redis.from_url(get_config()["REDIS_URL"], decode_responses=True)
    return redis