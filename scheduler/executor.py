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
        retry_wait: int = 5,
    ):
        self.session = session
        self.error_counts: Dict[str, int] = {}
        self.error_threshold = error_threshold
        self.rate_limit_wait = rate_limit_wait
        self.retry_wait = retry_wait
        self.notified_errors: Dict[str, bool] = {}

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
        - При других ошибках увеличивает счётчик этой ошибки и, если превышен порог,
          отправляет уведомление об ошибке только один раз с информацией о количестве повторений.
        """
        while True:
            try:
                async with self.session.post(
                    url, json=json, headers=headers, proxy=proxy
                ) as response:
                    if response.status == 200:
                        self.error_counts.clear()
                        self.notified_errors.clear()
                        return await response.json()

                    elif response.status == 429:
                        logger.warning(
                            "Получен статус 429 (rate limit). Ожидание %s секунд...",
                            self.rate_limit_wait,
                        )
                        await asyncio.sleep(self.rate_limit_wait)
                        continue
                    else:
                        key = f"HTTP_{response.status}"
                        self.error_counts[key] = self.error_counts.get(key, 0) + 1
                        response_text = await response.text()
                        logger.error(
                            "Получен HTTP статус %s. Ошибка %s повторений: %s",
                            response.status,
                            self.error_counts[key],
                            response_text,
                        )
                        if self.error_counts[key] >= self.error_threshold:
                            # Если уведомление для этого типа ошибки еще не отправлялось, отправляем один раз
                            if not self.notified_errors.get(key, False):
                                await self.notify_admin(key, self.error_counts[key])
                                self.notified_errors[key] = True
                            raise Exception(
                                f"Превышен порог ошибок для {key} (повторов: {self.error_counts[key]})"
                            )
                        await asyncio.sleep(self.retry_wait)
                        continue

            except aiohttp.ClientError as e:
                key = "ClientError"
                self.error_counts[key] = self.error_counts.get(key, 0) + 1
                logger.exception(
                    "ClientError. Ошибка %s повторений", self.error_counts[key]
                )
                if self.error_counts[key] >= self.error_threshold:
                    if not self.notified_errors.get(key, False):
                        await self.notify_admin(key, self.error_counts[key])
                        self.notified_errors[key] = True
                    raise
                await asyncio.sleep(self.retry_wait)

    async def notify_admin(self, error_identifier: str, count: int):
        """
        Отправляет уведомление администратору о постоянной ошибке всего один раз для каждого типа ошибки.
        Сообщение содержит тип ошибки и количество повторов.
        """
        message = f"Постоянная ошибка: {error_identifier} повторилась {count} раз."
        logger.error("Оповещаю администратора: %s", message)
        await bot.send_message(settings.ADMIN_ID, message)
