import uuid

from redis import WatchError

from rediska.manager.base import RedisManagerBase


class RedisManagerAccessTokens(RedisManagerBase):
    async def create_access_token(self, user_id: str | uuid.UUID) -> str:
        """
        Удаляет старые токены пользователя, создает новый, записывает и возвращает его

        Args:
            user_id: внутренний идентификатор пользователя

        Returns:
            (str) токен авторизации
        """
        async with self.redis.pipeline() as pipe:
            retries = 0
            while retries < 5:
                try:
                    retries += 1
                    await pipe.watch(f"access_tokens:user:{user_id}")

                    old_token = await pipe.get(f"access_tokens:user:{user_id}")
                    # Удаляем старый токен
                    if old_token:
                        await self.delete_access_token(old_token)
                    pipe.multi()
                    new_token = str(uuid.uuid4())
                    # Устанавливаем новые значения
                    await pipe.set(
                        f"access_tokens:token:{str(new_token)}",
                        str(user_id),
                        ex=60 * 60,
                    )
                    await pipe.set(
                        f"access_tokens:user:{str(user_id)}",
                        str(new_token),
                        ex=60 * 60 * 24,
                    )

                    await pipe.execute()

                    return new_token
                except WatchError:
                    continue

            raise RuntimeError("Failed to delete access token")

    async def get_user_id_by_access_token(
        self, access_token: str | uuid.UUID
    ) -> str | None:
        """
        Возвращает идентификатор пользователя по токену, если такой токен найден, иначе None

        Args:
            access_token: токен авторизации

        Returns:
            str | None
        """
        user_id = await self.redis.get(f"access_tokens:token:{str(access_token)}")
        return user_id

    async def delete_access_token(self, access_token) -> None:
        """
        Удаляет токен

        Args:
            access_token: какой токен нужно удалить

        Returns:
            None
        """
        async with self.redis.pipeline() as pipe:
            retries = 0
            while retries < 5:
                retries += 1
                try:
                    # Начинаем транзакцию
                    await pipe.watch(f"access_tokens:token:{str(access_token)}")

                    # Получаем user_id
                    user_id = await pipe.get(f"access_tokens:token:{access_token}")
                    pipe.multi()  # Начинаем блок multi/execute

                    if user_id:
                        await pipe.delete(f"access_tokens:token:{access_token}")
                        await pipe.delete(f"access_tokens:user:{user_id}")

                    # Исполняем транзакцию
                    await pipe.execute()
                    return
                except WatchError:
                    continue

        raise RuntimeError("Failed to delete access token")

    async def delete_access_token_by_user_id(self, user_id) -> None:
        """
        Удаляет все токены пользователя

        Args:
            user_id: какой пользователь

        Returns:
            None
        """
        async with self.redis.pipeline() as pipe:
            retries = 0
            while retries < 5:
                retries += 1
                try:
                    # Начинаем транзакцию
                    await pipe.watch(f"access_tokens:user:{user_id}")

                    # Получаем user_id
                    access_token = await pipe.get(f"access_tokens:user:{user_id}")
                    pipe.multi()  # Начинаем блок multi/execute

                    if access_token:
                        await pipe.delete(f"access_tokens:token:{access_token}")
                        await pipe.delete(f"access_tokens:user:{user_id}")

                    # Исполняем транзакцию
                    await pipe.execute()
                    return
                except WatchError:
                    continue

            raise RuntimeError("Failed to delete access token")
