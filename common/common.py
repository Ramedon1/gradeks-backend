from datetime import UTC, datetime

from sqlmodel import Field


def pg_now() -> datetime:
    return datetime.now().astimezone(UTC).replace(tzinfo=None)


def CreatedAtField(index=False):  # noqa
    return Field(
        default_factory=pg_now,
        nullable=False,
        index=index,
    )
