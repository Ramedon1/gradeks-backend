from rediska.manager.base import RedisManagerBase


class RedisManagerCache(RedisManagerBase):
    async def set_function_cache(self, name: str, value: str, expiration: int = 60):
        await self.redis.set(name, value, ex=expiration)

    async def set_function_lock(self, name: str, expiration: int = 2) -> bool:
        return await self.redis.set(name, "locked", nx=True, ex=expiration)

    async def delete_function_lock(self, name: str) -> None:
        await self.redis.delete(
            name,
        )

    async def get_function_cache(self, name: str) -> str | None:
        return await self.redis.get(name)

    async def get_keys(self, pattern: str) -> list[str]:
        return await self.redis.keys(pattern)

    async def delete_keys(self, keys: list[str]) -> None:
        return await self.redis.delete(*keys)

    async def drop_cache(self):
        keys = await self.redis.keys("caching:*")
        await self.redis.delete(*keys)
