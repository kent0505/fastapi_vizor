from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from core.db import Sql, get_db
from core.settings import settings
from routers.home import router as home_router
from routers.restaurant import router as restaurant_router
from routers.test import router as test_router
from routers.user import router as user_router
from routers.panorama import router as panorama_router

import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.info("STARTUP")
    async with get_db() as db:
        await db.execute(Sql.users)
        await db.execute(Sql.restaurants)
        await db.execute(Sql.panoramas)
        await db.execute(Sql.hotspots)
        await db.execute(Sql.reserves)
        await db.commit()
    yield
    logging.info("SHUTDOWN")

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

app.include_router(home_router, include_in_schema=False)
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(restaurant_router, prefix="/api/v1/restaurant", tags=["Restaurant"])
app.include_router(panorama_router, prefix="/api/v1/panorama", tags=["Panorama"])
app.include_router(test_router, prefix="/api/v1/test", tags=["Test"])

# pip install -r requirements.txt
# uvicorn main:app --reload

# WINDOWS
# python -m venv venv
# venv\Scripts\activate

# MAC | LINUX
# python3 -m venv venv
# source venv/bin/activate
# lsof -t -i tcp:8000 | xargs kill -9

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/api/v1/test/
