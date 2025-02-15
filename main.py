from fastapi import FastAPI, APIRouter, Request
import uvicorn
from app.apis import request_routes
from contextvars import ContextVar
from app.middlewares.context import request_context
import uuid

# import gunicorn

app = FastAPI()


app.include_router(request_routes.router, prefix="/api")

@app.middleware("http")
async def set_request_context(request: Request, call_next):
    request.state.newid = str(uuid.uuid4())
    request_context.set(request)
    try:
        response = await call_next(request)
    finally:
        # Clear the context variable after the request is processed
        request_context.set(None)
    return response

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)