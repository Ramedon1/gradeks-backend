import time

from rediska.manager.base import RedisManagerBase


class RedisManagerNewGrades(RedisManagerBase):
    GRADE_TTL_SECONDS = 86400

    async def add_new_grade_to_redis(
        self,
        user_id: str,
        subject: str,
        grading_date: str,
        grade: int,
        grade_weight: int,
    ):
        """Add a new grade to Redis and set TTL to 1 day."""
        times = int(time.time())
        await self.redis.hset(
            f"user:{user_id}:grade:{times}",
            mapping={
                "subject": subject,
                "grading_date": grading_date,
                "new_grade": grade,
                "grade_weight": grade_weight,
            },
        )
        await self.redis.expire(f"user:{user_id}:grade:{times}", self.GRADE_TTL_SECONDS)

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
        await self.redis.expire(f"user:{user_id}:grade:{times}", self.GRADE_TTL_SECONDS)

    async def get_all_new_grades(self, user_id):
        """Get all new grades from Redis."""
        keys = await self.redis.keys(f"user:{user_id}:grade:*")
        grades = []
        for key in keys:
            grades.append(await self.redis.hgetall(key))
        return grades if grades else None
