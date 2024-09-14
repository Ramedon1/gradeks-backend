import hashlib
import hmac
from datetime import datetime
from operator import itemgetter
from urllib.parse import parse_qsl

from pydantic import BaseModel, Field, field_validator

import settings
from common import context_logger
from web.models.users.telegram import WebAppInitData as TelegramData

logger = context_logger.get(__name__)


class LoginRequest(BaseModel):
    telegram_data: TelegramData
    version: str
    platform: str

    @field_validator("telegram_data", mode="before")  # noqa
    @classmethod
    def validate_telegram_data(cls, value: str) -> TelegramData:
        try:
            parsed_data = dict(parse_qsl(value, strict_parsing=True))
        except ValueError:  # pragma: no cover
            # Init data is not a valid query string
            raise ValueError("Init data is not a valid query string")
        if "hash" not in parsed_data:
            # Hash is not present in init data
            raise ValueError("Hash is not present in init data")
        hash_ = parsed_data.pop("hash")

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=settings.BOT_TOKEN.encode(), digestmod=hashlib.sha256
        )
        calculated_hash = hmac.new(
            key=secret_key.digest(),
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        if calculated_hash == hash_:
            return TelegramData.model_validate(parsed_data | {"hash": hash_})
        raise ValueError("Invalid hash")


class LoginResponse(BaseModel):
    server_time: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000)
    )
    access_token: str
