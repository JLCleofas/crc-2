from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse

from backend.middleware.log_middleware import log_middleware
from backend.core.logger import logger
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware


app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
logger.info('Starting application')
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="backend/templates")

@app.get("/")
async def root(request: Request):
    return  templates.TemplateResponse("base.html", {"request": request})

@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/health", status_code=200, description="Health check")
async def health():
    return {"health": "ok"}
