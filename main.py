from fastapi             import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from contextlib          import asynccontextmanager
from dotenv              import load_dotenv
from core.db             import get_db
from core.settings       import settings
from core.security       import JWTBearer, Roles
from db import (
    user,
    restaurant,
    panorama,
    hotspot,
    menu,
)
from routers.home        import router as home_router
from routers.client      import router as client_router
from routers.user        import router as user_router
from routers.restaurant  import router as restaurant_router
from routers.panorama    import router as panorama_router
from routers.hotspots    import router as hotspots_router
from routers.menu        import router as menu_router

import logging

@asynccontextmanager
async def lifespan(_: FastAPI):
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    async with get_db() as db:
        await db.execute(user.User.CREATE)
        await db.execute(restaurant.Restaurant.CREATE)
        await db.execute(panorama.Panorama.CREATE)
        await db.execute(hotspot.Hotspot.CREATE)
        await db.execute(menu.Menu.CREATE)
        await db.commit()
    yield

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.mount(path="/static",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

ADMIN = [Depends(JWTBearer())]
STUFF = [Depends(JWTBearer(role=Roles.stuff))]
USER =  [Depends(JWTBearer(role=Roles.user))]

app.include_router(home_router, include_in_schema=False)
app.include_router(user_router,       prefix="/api/v1/user",       tags=["User"])
app.include_router(client_router,     prefix="/api/v1/client",     tags=["Client"],     dependencies=USER)
app.include_router(restaurant_router, prefix="/api/v1/restaurant", tags=["Restaurant"], dependencies=ADMIN)
app.include_router(panorama_router,   prefix="/api/v1/panorama",   tags=["Panorama"],   dependencies=ADMIN)
app.include_router(hotspots_router,   prefix="/api/v1/hotspot",    tags=["Hotspot"],    dependencies=ADMIN)
app.include_router(menu_router,       prefix="/api/v1/menu",       tags=["Menu"],       dependencies=ADMIN)

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
# https://s3.twcstorage.ru/85a1cfc8-10bb0390-23dd-464a-806a-6301ca90db7b/restaurants/1.jpg
