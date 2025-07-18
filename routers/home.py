from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.db import (
    db_get_users,
    db_get_restaurants,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    users = await db_get_users()
    restaurants = await db_get_restaurants()

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "restaurants": restaurants,
        }
    )
