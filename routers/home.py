from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.security import Roles
from db import SessionDep
from db.user import User, db_get_users
from db.city import db_get_cities
from db.restaurant import db_get_restaurants
from db.panorama import db_get_panoramas
from db.hotspot import db_get_hotspots
from db.category import db_get_categories
from db.menu import db_get_menus

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(
    request: Request,
    db: SessionDep,
):
    users = await db_get_users(db)
    cities = await db_get_cities(db)
    restaurants = await db_get_restaurants(db)
    panoramas = await db_get_panoramas(db)
    hotspots = await db_get_hotspots(db)
    categories = await db_get_categories(db)
    menus = await db_get_menus(db)

    if not users:
        user = User(
            name="Otabek",
            phone="+998998472580",
            age=25,
            role=Roles.admin.value,
        )
        db.add(user)
        await db.commit()

        users = await db_get_users(db)

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "cities": cities,
            "restaurants": restaurants,
            "panoramas": panoramas,
            "hotspots": hotspots,
            "categories": categories,
            "menus": menus,
        }
    )
