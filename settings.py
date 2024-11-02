import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "gradeks")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASS = os.getenv("POSTGRES_PASS", "password")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = os.getenv("REDIS_HOST", "")
REDIS_PORT = os.getenv("REDIS_PORT", "")
REDIS_USER = os.getenv("REDIS_USER", "")
REDIS_PASS = os.getenv("REDIS_PASS", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

WEB_UI_URL = os.getenv("WEB_UI_URL", "")

PROXY_URL = os.getenv("PROXY_URL", "")
ADMIN_ID = os.getenv("ADMIN_ID", "")
