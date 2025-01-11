import asyncio
import json
import logging
from datetime import date, datetime, timedelta

import aiohttp
from fake_useragent import UserAgent

import settings
from scheduler.models import Grade, GradeFinal, NewGrade, Period

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


async def get_final_grades(diary_id: str) -> list[GradeFinal]:
    data = {
        "apikey": "ytokgwebvrxughawekfinvpusbvp",
        "guid": diary_id,
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Host": "mp.edu.orb.ru",
        "Connection": "Keep-Alive",
        "User-Agent": UserAgent().random,
        "Accept-Encoding": "gzip, deflate, br",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "https://mp.edu.orb.ru/journals/periodmarks",
            json=data,
            proxy=proxy_url,
        ) as response:
            if response.status == 200:
                try:
                    result = await response.json()
                    if "data" not in result:
                        logger.error("Response does not contain 'data' key")
                        logger.debug(f"Full response: {result}")
                        return []

                    final_grades = []
                    for subject_data in result["data"]:
                        subject_name = subject_data["NAME"]
                        periods = []

                        for period_data in subject_data["PERIODS"]:
                            grades = []
                            mark = period_data.get("MARK")

                            if mark:
                                grades.append(
                                    Grade(
                                        date=None,
                                        grade=mark["VALUE"],
                                        weight=mark["WEIGHT"],
                                    )
                                )

                            periods.append(
                                Period(
                                    name=period_data["NAME"],
                                    date_begin=period_data["DATE_BEGIN"],
                                    date_end=period_data["DATE_END"],
                                    grades=grades if grades else None,
                                )
                            )

                        final_grades.append(
                            GradeFinal(subject=subject_name, periods=periods)
                        )
                    return final_grades

                except Exception as e:
                    logger.exception(f"Error parsing response: {e}")
                    logger.debug(f"Response content: {await response.text()}")
                    return []

            else:
                logger.error(f"Unexpected response status: {response.status}")
                logger.debug(f"Response content: {await response.text()}")
                return []