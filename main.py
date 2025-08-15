from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles     import StaticFiles
from faststream.rabbit.fastapi import RabbitRouter
from contextlib              import asynccontextmanager
from core.bot                import start_bot
from core.config             import settings
from db                      import create_all, dispose_db
from routers.home            import router as home_router
from routers.auth            import router as auth_router
from routers.client          import router as client_router
from routers.user            import router as user_router
from routers.admin           import router as admin_router
from routers.city            import router as city_router
from routers.restaurant      import router as restaurant_router
from routers.panorama        import router as panorama_router
from routers.hotspot         import router as hotspot_router
from routers.category        import router as category_router
from routers.menu            import router as menu_router

import logging
import asyncio
import uvicorn

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=logging.INFO)
    await create_all()
    bot_task = asyncio.create_task(start_bot())
    yield
    bot_task.cancel()
    await dispose_db()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

app.add_middleware(
    middleware_class  = CORSMiddleware, 
    allow_origins     = ["*"], 
    allow_methods     = ["*"], 
    allow_headers     = ["*"],
    allow_credentials = True, 
)

app.mount(path="/static",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

app.include_router(home_router, include_in_schema=False)
app.include_router(auth_router,       prefix="/api/v1/auth",       tags=["Auth"])
app.include_router(client_router,     prefix="/api/v1/client",     tags=["Client"])
app.include_router(user_router,       prefix="/api/v1/user",       tags=["User"])
app.include_router(admin_router,      prefix="/api/v1/admin",      tags=["Admin"])
app.include_router(city_router,       prefix="/api/v1/city",       tags=["City"])
app.include_router(restaurant_router, prefix="/api/v1/restaurant", tags=["Restaurant"])
app.include_router(panorama_router,   prefix="/api/v1/panorama",   tags=["Panorama"])
app.include_router(hotspot_router,    prefix="/api/v1/hotspot",    tags=["Hotspot"])
app.include_router(category_router,   prefix="/api/v1/category",   tags=["Category"])
app.include_router(menu_router,       prefix="/api/v1/menu",       tags=["Menu"])

router = RabbitRouter(url=settings.rabbit_url)

@router.post("/order")
async def test(name: str):
    await router.broker.publish(
        f"New orders: {name}",
        queue="orders",
    )
    return {"message": "OK"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app", 
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

# python main.py
# uvicorn main:app --reload
# docker-compose up --build
# pip install -r requirements.txt

# WINDOWS
# python -m venv venv
# venv\Scripts\activate

# MAC | LINUX
# python3 -m venv venv
# source venv/bin/activate
# lsof -t -i tcp:8000 | xargs kill -9
