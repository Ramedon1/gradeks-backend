from redis.asyncio import Redis


class RedisManagerBase:
    def __init__(self, connection: Redis):
        self.redis = connection
