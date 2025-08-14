from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.security import Roles
from db import SessionDep
from db.user import User, db_get_users

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(
    request: Request,
    db: SessionDep,
):
    users = await db_get_users(db)
    # cities = await db_get_cities()
    # restaurants = await db_get_restaurants()

    if not users:
        user = User(
            name="Otabek",
            phone="+998998472580",
            age=25,
            role=Roles.admin,
        )
        db.add(user)
        await db.commit()

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
