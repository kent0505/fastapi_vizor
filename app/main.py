from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from core.config import settings
from db import engine
from home import router as home_router
from api.v1 import router as v1_router

import uvicorn
import logging

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=logging.INFO)
    yield
    await engine.dispose()

app = FastAPI(
    lifespan=lifespan,
    title="Vizor",
    description=settings.jwt.admin,
    swagger_ui_parameters=settings.swagger.ui_parameters,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)

app.include_router(home_router, include_in_schema=False)
app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

# pip install -r requirements.txt

# DOCKER
# docker-compose up -d
# docker build -t fastapi .
# docker run -p 8000:8000 fastapi

# ALEMBIC
# alembic init migrations
# alembic revision --autogenerate -m "xyz"
# alembic upgrade head

# WINDOWS
# python -m venv venv
# venv\Scripts\activate

# MAC | LINUX
# python3 -m venv venv
# source venv/bin/activate
# lsof -t -i tcp:8000 | xargs kill -9
