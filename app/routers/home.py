from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from db import SessionDep, select
from db.user import User
from db.city import City
from db.restaurant import Restaurant
from db.panorama import Panorama
from db.hotspot import Hotspot
from db.category import Category
from db.menu import Menu

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(
    request: Request,
    db: SessionDep,
):
    users = (await db.scalars(select(User))).all()
    cities = (await db.scalars(select(City))).all()
    restaurants = (await db.scalars(select(Restaurant))).all()
    panoramas = (await db.scalars(select(Panorama))).all()
    hotspots = (await db.scalars(select(Hotspot))).all()
    categories = (await db.scalars(select(Category))).all()
    menus = (await db.scalars(select(Menu))).all()

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
