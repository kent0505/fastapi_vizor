from fastapi import APIRouter
from db import SessionDep
from db.city import db_get_cities
from db.restaurant import db_get_restaurants_by_city
from db.panorama import db_get_panoramas_by_rid
from db.hotspot import db_get_hotspots_by_pid
from db.category import db_get_categories
from db.menu import db_get_menus_by_restaurant

router = APIRouter()

@router.get("/cities")
async def get_cities(db: SessionDep):
    cities = await db_get_cities(db)

    return {"cities": cities}

@router.get("/restaurants")
async def get_restaurants(
    city: int,
    db: SessionDep,
):
    restaurants = await db_get_restaurants_by_city(db, city)

    return {
        "city": city,
        "restaurants": restaurants,
    }

@router.get("/panoramas")
async def get_panoramas(
    rid: int,
    db: SessionDep,
):
    panoramas = await db_get_panoramas_by_rid(db, rid)

    return {
        "rid": rid,
        "panoramas": panoramas,
    }

@router.get("/hotspots")
async def get_hotspots(
    pid: int,
    db: SessionDep,
):
    hotspots = await db_get_hotspots_by_pid(db, pid)

    return {
        "pid": pid,
        "hotspots": hotspots,
    }

@router.get("/categories")
async def get_categories(db: SessionDep):
    categories = await db_get_categories(db)

    return {"categories": categories}

@router.get("/menus")
async def get_menus(
    rid: int,
    db: SessionDep,
):
    menus = await db_get_menus_by_restaurant(db, rid)

    return {
        "rid": rid,
        "menus": menus,
    }
