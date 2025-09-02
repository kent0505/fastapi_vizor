from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from db import SessionDep, select
from db.user import User
from db.city import City
from db.restaurant import Restaurant
from db.panorama import Panorama
from db.table import RestaurantTable
from db.hotspot import Hotspot
from db.category import Category
from db.menu import Menu
from db.flower import Flower
from db.flower_order import FlowerOrder

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(
    request: Request,
    db: SessionDep,
):
    users = (await db.scalars(select(User))).all()
    cities = (await db.scalars(
        select(City)
        .order_by(
            City.position.desc(), 
            City.id.asc(),
        ),
    )).all()
    restaurants = (await db.scalars(
        select(Restaurant)
        .order_by(
            Restaurant.position.desc(), 
            Restaurant.id.asc(),
        ),
    )).all()
    panoramas = (await db.scalars(select(Panorama))).all()
    tables = (await db.scalars(select(RestaurantTable))).all()
    hotspots = (await db.scalars(select(Hotspot))).all()
    categories = (await db.scalars(select(Category))).all()
    menus = (await db.scalars(select(Menu))).all()
    flowers = (await db.scalars(select(Flower))).all()
    flower_orders = (await db.scalars(select(FlowerOrder))).all()

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "cities": cities,
            "restaurants": restaurants,
            "panoramas": panoramas,
            "tables": tables,
            "hotspots": hotspots,
            "categories": categories,
            "menus": menus,
            "flowers": flowers,
            "flower_orders": flower_orders,
        }
    )
