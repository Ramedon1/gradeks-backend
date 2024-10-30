import time
import uuid

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import settings
from common import context_logger
from common.context_logger import SpanId, TraceId
from web.routes.distribution import distribution_router
from web.routes.grade import grade_router
from web.routes.users import user_router

logger = context_logger.get(__name__)

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


fastapi_app.include_router(user_router)
fastapi_app.include_router(distribution_router)
fastapi_app.include_router(grade_router)



@fastapi_app.options("/{path:path}")
async def preflight_handler():
    return JSONResponse(status_code=200, content="OK")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://gradeks.xyz",
    "https://api.gradeks.xyz",
    "*",
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
