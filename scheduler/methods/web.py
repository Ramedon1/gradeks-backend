import json
import logging
from datetime import date, datetime, timedelta

import aiohttp
from fake_useragent import UserAgent

import settings
from scheduler.models import Grade, NewGrade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

proxy_url = settings.PROXY_URL


async def get_grades_by_period(
    diary_id: str, from_date: date, to_date: date
) -> list[NewGrade]:
    data = {
        "apikey": "ytokgwebvrxughawekfinvpusbvp",
        "guid": diary_id,
        "from": from_date.strftime("%d.%m.%Y"),
        "to": to_date.strftime("%d.%m.%Y"),
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Host": "mp.edu.orb.ru",
        "Connection": "Keep-Alive",
        "User-Agent": UserAgent().random,
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Length": str(len(json.dumps(data))),
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "https://mp.edu.orb.ru/journals/marksbyperiod",
            json=data,
            proxy=proxy_url,
        ) as response:
            if response.status == 200:
                result = await response.json()
                if "data" in result:
                    grades_by_subject = []

                    for item in result["data"]:
                        subject = item["SUBJECT_NAME"]
                        grades = []
                        occupied_dates = set()

                        for mark in item["MARKS"]:
                            grade_date = datetime.strptime(
                                mark["DATE"], "%d.%m.%Y"
                            ).date()

                            while grade_date in occupied_dates:
                                grade_date += timedelta(days=1)

                            occupied_dates.add(grade_date)

                            grade = Grade(
                                date=grade_date.isoformat(),
                                grade=mark["VALUE"],
                                weight=mark["WEIGHT"],
                            )

                            grades.append(grade)

                        grades_by_subject.append(
                            NewGrade(subject=subject, grades=grades)
                        )
                    return grades_by_subject
            else:
                logger.error(f"Unexpected response status: {response.status}")
                logger.debug(f"Response content: {await response.text()}")

    logger.warning("No grades returned.")
    return []
