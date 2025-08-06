from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.security import Roles
from db.city import db_get_cities
from db.restaurant import db_get_restaurants
from db.user import (
    User,
    db_add_user,
    db_get_users,
)

import logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    users = await db_get_users()
    cities = await db_get_cities()
    restaurants = await db_get_restaurants()

    if not users:
        await db_add_user(
            role=Roles.admin,
            user=User(
                name="Otabek",
                phone="+998998472580",
                age=25,
            ),
        )
        users = await db_get_users()

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "cities": cities,
            "restaurants": restaurants,
            # "panoramas": panoramas,
            # "hotspots": hotspots,
            # "menus": menus,
        }
    )
