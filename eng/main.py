from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from routers.broker import router as broker_router

import uvicorn
import logging

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=logging.INFO)
    # await db_helper.create_all()
    yield
    # await db_helper.dispose()

app = FastAPI(
    title="English",
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(broker_router, prefix="/api/v1/broker", tags=["Broker"])

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
