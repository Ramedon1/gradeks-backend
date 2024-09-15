from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import NoBackoff

import settings

connection = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASS,
    username=settings.REDIS_USER,
    decode_responses=True,
    retry=Retry(NoBackoff(), 5),
    retry_on_timeout=True,
    health_check_interval=5,
)
