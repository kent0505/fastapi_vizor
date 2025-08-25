from fastapi import APIRouter
from db import SessionDep, select
from db.city import City
from db.restaurant import Restaurant
from db.panorama import Panorama
from db.table import RestaurantTable
from db.hotspot import Hotspot
from db.category import Category
from db.menu import Menu

router = APIRouter()

@router.get("/cities")
async def get_cities(db: SessionDep):
    cities = (await db.scalars(select(City))).all()

    return {"cities": cities}

@router.get("/restaurants")
async def get_restaurants(
    city: int,
    db: SessionDep,
):
    restaurants = (await db.scalars(select(Restaurant).filter_by(city=city))).all()

    return {"restaurants": restaurants}

@router.get("/panoramas")
async def get_panoramas(
    rid: int,
    db: SessionDep,
):
    panoramas = (await db.scalars(select(Panorama).filter_by(rid=rid))).all()

    return {"panoramas": panoramas}

@router.get("/tables")
async def get_tables(
    rid: int,
    db: SessionDep,
):
    tables = (await db.scalars(select(RestaurantTable).filter_by(rid=rid))).all()

    return {"tables": tables}

@router.get("/hotspots")
async def get_hotspots(
    rid: int,
    db: SessionDep,
):
    hotspots = (await db.scalars(select(Hotspot).filter_by(rid=rid))).all()

    return {"hotspots": hotspots}

@router.get("/categories")
async def get_categories(db: SessionDep):
    categories = (await db.scalars(select(Category))).all()

    return {"categories": categories}

@router.get("/menus")
async def get_menus(
    rid: int,
    db: SessionDep,
):
    menus = (await db.scalars(select(Menu).filter_by(rid=rid))).all()

    return {"menus": menus}
