from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from core.security import Roles
from db import AsyncSession, db_helper
from db.user import (
    User,
    db_add_user,
    db_get_users,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(
    request: Request,
    db: AsyncSession = Depends(db_helper.get_db),
):
    users = await db_get_users(db)
    # cities = await db_get_cities()
    # restaurants = await db_get_restaurants()

    if not users:
        await db_add_user(
            db,
            user=User(
                name="Otabek",
                phone="+998998472580",
                age=25,
                role=Roles.admin,
            ),
        )
        users = await db_get_users(db)

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            # "cities": cities,
            # "restaurants": restaurants,
            # "panoramas": panoramas,
            # "hotspots": hotspots,
            # "menus": menus,
        }
    )
