from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.db import (
    db_get_users,
    db_get_restaurants,
    db_get_panoramas,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    users = await db_get_users()
    restaurants = await db_get_restaurants()
    panoramas = await db_get_panoramas()

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "restaurants": restaurants,
            "panoramas": panoramas,
        }
    )
