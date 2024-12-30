import asyncio
import time
from datetime import datetime, timedelta

import pytz

from rediska.manager.base import RedisManagerBase


class RedisManagerNewGrades(RedisManagerBase):
    async def add_new_grade_to_redis(
        self,
        user_id: str,
        subject: str,
        grading_date: str | None,
        grade: int,
        grade_weight: int,
        is_final: bool = False,
    ):
        """Add a new grade to Redis and set TTL to expire at midnight Ekaterinburg time."""

        ekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")
        now = datetime.now(ekaterinburg_tz)
        next_midnight = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        ttl_seconds = int((next_midnight - now).total_seconds())
        times = int(time.time())
        await self.redis.hset(
            f"user:{user_id}:grade:{times}",
            mapping={
                "subject": subject,
                "grading_date": str(grading_date),
                "new_grade": grade,
                "grade_weight": grade_weight,
                "is_final": str(is_final),
            },
        )

        await self.redis.expire(f"user:{user_id}:grade:{times}", ttl_seconds)

    async def update_grade_in_redis(
        self,
        user_id: str,
        subject: str,
        grading_date: str,
        new_grade: int,
        old_grade: int | None,
        grade_weight: int,
    ):
        """Update an existing grade in Redis, logging both the new and old grade values, and set TTL to 1 day."""
        ekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")
        now = datetime.now(ekaterinburg_tz)
        next_midnight = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        ttl_seconds = int((next_midnight - now).total_seconds())
        times = int(time.time())
        await self.redis.hset(
            f"user:{user_id}:grade:{times}",
            mapping={
                "subject": subject,
                "grading_date": grading_date,
                "new_grade": new_grade,
                "old_grade": old_grade,
                "grade_weight": grade_weight,
            },
        )
        await self.redis.expire(f"user:{user_id}:grade:{times}", ttl_seconds)

    async def get_all_new_grades(self, user_id):
        """Get all new grades from Redis."""
        keys = await self.redis.keys(f"user:{user_id}:grade:*")
        grades = []
        for key in keys:
            grades.append(await self.redis.hgetall(key))
        return grades if grades else None

    async def delete_all_grades_for_user(self, user_id):
        """Delete all grades for a user from Redis."""
        keys = await self.redis.keys(f"user:{user_id}:grade:*")
        if keys:
            await self.redis.delete(*keys)
        return True
