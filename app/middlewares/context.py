from contextvars import ContextVar
from fastapi import Request

# Create a context variable to store the request
request_context: ContextVar[Request] = ContextVar("request_context", default=None)