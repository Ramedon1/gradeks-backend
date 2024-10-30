import aiohttp
import asyncio

async def get_grades(diary_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://mp.edu.orb.ru/journals/allperiods") as response:
            print(await response.text())


asyncio.run(get_grades("123"))