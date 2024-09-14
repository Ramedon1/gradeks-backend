import time
import uuid

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

import settings
from common.context_logger import SpanId, TraceId

# Здесь прописать роуты чтобы потом иметь доступ к им доксам

fastapi_app = FastAPI()


@fastapi_app.middleware("http")
async def add_process_time_header_and_trace_id(request: Request, call_next):
    trace_id_token = TraceId.set(str(uuid.uuid4()))
    span_id_token = SpanId.set(str(uuid.uuid4()))
    start_time = time.monotonic()

    response = await call_next(request)
    process_time = time.monotonic() - start_time

    response.headers["X-Trace-Id"] = str(TraceId.get())
    response.headers["X-Process-Time"] = str(process_time)
    TraceId.reset(trace_id_token)
    SpanId.reset(span_id_token)
    return response


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    settings.WEB_UI_URL.strip("/"),
    "*",
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
