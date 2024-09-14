import logging
from contextvars import ContextVar
from typing import Any

TraceId: ContextVar[str] = ContextVar("trace_id")
SpanId: ContextVar[str] = ContextVar("span_id")
Context: ContextVar[dict[str, Any]] = ContextVar("context")


class ContextAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        if TraceId.get(None):
            kwargs.setdefault("extra", {})["trace_id"] = TraceId.get()
        if SpanId.get(None):
            kwargs.setdefault("extra", {})["span_id"] = SpanId.get()

        try:
            context = Context.get()
        except LookupError:
            return msg, kwargs

        for key, value in context.items():
            kwargs.setdefault("extra", {})[key] = value

        return msg, kwargs


def get(name: str) -> ContextAdapter:
    return ContextAdapter(logging.getLogger(name), {})
