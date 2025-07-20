from fastapi import APIRouter
from core.db import (
    db_get_users,
    db_get_restaurants,
    db_get_panoramas,
    db_get_hotspots,
    db_get_menus,
)

router = APIRouter()

@router.get("/")
async def test():
    users = await db_get_users()
    restaurants = await db_get_restaurants()
    panoramas = await db_get_panoramas()
    hotspots = await db_get_hotspots()
    menus = await db_get_menus()

    return {
        "users": users,
        "restaurants": restaurants,
        "panoramas": panoramas,
        "hotspots": hotspots,
        "menus": menus,
    }
