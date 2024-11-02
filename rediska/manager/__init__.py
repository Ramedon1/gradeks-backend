from redis.asyncio import Redis

from rediska.manager.access_tokens import RedisManagerAccessTokens
from rediska.manager.new_grades import RedisManagerNewGrades


class RedisManager:
    def __init__(self, connection: Redis):
        self._is_stopped: bool = True
        self._connection: Redis = connection
        self.access_tokens: RedisManagerAccessTokens = RedisManagerAccessTokens(
            connection
        )
        self.new_grades: RedisManagerNewGrades = RedisManagerNewGrades(connection)

    async def start(self) -> None:
        if self._is_stopped is False:
            raise ValueError("Already started")
        await self._connection.initialize()
        self._is_stopped = False

    async def close(self) -> None:
        if self._is_stopped is True:
            raise ValueError("Already closed")
        await self._connection.aclose()
        self._is_stopped = True
