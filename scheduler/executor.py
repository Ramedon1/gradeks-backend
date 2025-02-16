import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp

import settings
from tg.bot import bot

logger = logging.getLogger(__name__)

class SafeRequestExecutor:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        error_threshold: int = 3,
        rate_limit_wait: int = 60,
        retry_wait: int = 5
    ):
        self.session = session
        self.error_counts: Dict[str, int] = {}
        self.error_threshold = error_threshold
        self.rate_limit_wait = rate_limit_wait
        self.retry_wait = retry_wait

    async def post(
        self,
        url: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
    ) -> Any:
        """
        Выполняет POST-запрос с обработкой ошибок.

        - При статусе 429 ждёт rate_limit_wait секунд и повторяет запрос.
        - При других ошибках увеличивает счётчик этой ошибки и, если превышен порог, оповещает администратора и прекращает попытки.
        """
        while True:
            try:
                async with self.session.post(url, json=json, headers=headers, proxy=proxy) as response:
                    if response.status == 200:
                        self.error_counts.clear()
                        return await response.json()

                    elif response.status == 429:
                        logger.warning("Получен статус 429 (rate limit). Ожидание %s секунд...", self.rate_limit_wait)
                        await asyncio.sleep(self.rate_limit_wait)
                        continue
                    else:
                        key = f"HTTP_{response.status}"
                        self.error_counts[key] = self.error_counts.get(key, 0) + 1
                        logger.error("Получен HTTP статус %s. Ошибка %s повторений: %s", response.status, self.error_counts[key], await response.text())
                        if self.error_counts[key] >= self.error_threshold:
                            await self.notify_admin(key)
                            raise Exception(f"Превышен порог ошибок для {key}")
                        await asyncio.sleep(self.retry_wait)
                        continue

            except aiohttp.ClientError as e:
                key = f"ClientError: {str(e)}"
                self.error_counts[key] = self.error_counts.get(key, 0) + 1
                logger.exception("ClientError: %s. Ошибка %s повторений", e, self.error_counts[key])
                if self.error_counts[key] >= self.error_threshold:
                    await self.notify_admin(key)
                    raise
                await asyncio.sleep(self.retry_wait)

    async def notify_admin(self, error_identifier: str):
        """
        Оповещает администратора о постоянной ошибке.
        Здесь можно реализовать отправку уведомления через Telegram или другой канал.
        """
        logger.error("Оповещаю администратора о постоянной ошибке: %s", error_identifier)
        await bot.send_message(settings.ADMIN_ID, f"Постоянная ошибка: {error_identifier}")
        pass
