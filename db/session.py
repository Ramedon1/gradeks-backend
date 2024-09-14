from sqlalchemy.ext.asyncio import create_async_engine

import settings

engine = create_async_engine(settings.POSTGRES_URL, pool_pre_ping=True)
