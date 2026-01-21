from idlelib.debugobj import dispatch

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.middleware.log_middleware import log_middleware
from backend.core.logger import logger


app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
logger.info('Starting application')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/health", status_code=200, description="Health check")
async def health():
    return {"health": "ok"}
