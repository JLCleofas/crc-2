from fastapi import FastAPI, Request, Form
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

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
    theme_color = request.cookies.get("theme")
    return  templates.TemplateResponse("base.html", {"request": request, "theme_color": theme_color})

@app.get("/home")
async def home(request: Request):
    theme_color = request.cookies.get("theme")
    return templates.TemplateResponse("pages/home.html", {"request": request, "theme_color": theme_color})

@app.post("/theme")
async def set_theme(request: Request, theme: str = Form(...)):
    allowed = {"light", "dark"}
    if theme not in allowed:
        return Response(status_code=400, content={"message": "Invalid theme"})

    resp = Response(status_code=204)

    resp.set_cookie(key="theme",
                    value=theme,
                    max_age=86400,
                    samesite="lax",
                    secure=False, # set to True on PROD
                    httponly=False,
                    )

    return resp

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/health", status_code=200, description="Health check")
async def health():
    return {"health": "ok"}
