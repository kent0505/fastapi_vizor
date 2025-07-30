from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.db import Tables, db_get_list

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    users = await db_get_list(Tables.users)
    restaurants = await db_get_list(Tables.restaurants)
    panoramas = await db_get_list(Tables.panoramas)
    hotspots = await db_get_list(Tables.hotspots)
    menus = await db_get_list(Tables.menus)

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "restaurants": restaurants,
            "panoramas": panoramas,
            "hotspots": hotspots,
            "menus": menus,
        }
    )
