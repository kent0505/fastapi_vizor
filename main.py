from fastapi             import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib          import asynccontextmanager
from dotenv              import load_dotenv
from bot                 import start_bot
from settings            import settings
from routers.home        import router as home_router
from routers.test        import router as test_router

import logging
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.info("STARTUP")
    bot_task = asyncio.create_task(start_bot())
    yield
    # shutdown
    logging.info("SHUTDOWN")
    bot_task.cancel()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(home_router, include_in_schema=False)
app.include_router(test_router, prefix="/api/v1/test", tags=["Test"])

# pip install -r requirements.txt
# uvicorn main:app --reload

# WINDOWS
# python -m venv venv
# venv\Scripts\activate

# MAC | LINUX
# python3 -m venv venv
# source venv/bin/activate
# sudo lsof -t -i tcp:8000 | xargs kill -9

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/api/v1/test/
