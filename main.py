from fastapi             import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib          import asynccontextmanager
from core.bot            import start_bot
from core.settings       import settings
from routers.home        import router as home_router
from routers.auth        import router as auth_router
from routers.user        import router as user_router
from routers.admin       import router as admin_router
from routers.photo       import router as photo_router
from routers.client      import router as client_router
from routers.restaurant  import router as restaurant_router
from routers.panorama    import router as panorama_router
from routers.hotspots    import router as hotspots_router
from routers.menu        import router as menu_router
from db                  import (
    get_db,
    user,
    restaurant,
    panorama,
    hotspot,
    menu,
)

import logging
import asyncio

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=logging.INFO)
    # bot_task = asyncio.create_task(start_bot())
    async with get_db() as db:
        await db.execute(user.User.CREATE)
        # await db.execute(restaurant.Restaurant.CREATE)
        # await db.execute(panorama.Panorama.CREATE)
        # await db.execute(hotspot.Hotspot.CREATE)
        # await db.execute(menu.Menu.CREATE)
        await db.commit()
    yield
    # bot_task.cancel()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.mount(path="/static",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

app.include_router(home_router, include_in_schema=False)
app.include_router(auth_router,       prefix="/api/v1/auth",       tags=["Auth"])
app.include_router(user_router,       prefix="/api/v1/user",       tags=["User"])
app.include_router(admin_router,      prefix="/api/v1/admin",      tags=["Admin"])
app.include_router(photo_router,      prefix="/api/v1/photo",      tags=["Photo"])
# app.include_router(client_router,     prefix="/api/v1/client",     tags=["Client"])
# app.include_router(restaurant_router, prefix="/api/v1/restaurant", tags=["Restaurant"])
# app.include_router(panorama_router,   prefix="/api/v1/panorama",   tags=["Panorama"])
# app.include_router(hotspots_router,   prefix="/api/v1/hotspot",    tags=["Hotspot"])
# app.include_router(menu_router,       prefix="/api/v1/menu",       tags=["Menu"])

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
