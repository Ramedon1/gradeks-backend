import asyncio

import uvicorn

from tg import bot
from tg.dispatcher import dp
from web.app import fastapi_app


async def main() -> None:
    config = uvicorn.Config(fastapi_app, host="0.0.0.0")
    server = uvicorn.Server(config)

    await server.serve()


asyncio.run(main())
