from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.s3 import delete_object
from db import AsyncSession, db_helper
from db.city import db_get_city_by_id
from db.restaurant import (
    Restaurant,
    RestaurantBody,
    db_get_restaurant_by_id,
    db_add_restaurant,
    db_delete_restaurant,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_restaurant(
    body: RestaurantBody,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_city_by_id(db, body.city)
    if not row:
        raise HTTPException(404, "city not found")

    restaurant = Restaurant(
        title=body.title,
        phone=body.phone,
        address=body.address,
        latlon=body.latlon,
        hours=body.hours,
        position=body.position,
        city=body.city,
        status=body.status,   
    )
    await db_add_restaurant(db, restaurant)

    return {"message": "restaurant added"}

@router.put("/")
async def edit_restaurant(
    body: RestaurantBody,
    db: AsyncSession = Depends(db_helper.get_db),
):
    restaurant = await db_get_restaurant_by_id(db, body.id)
    if not restaurant:
        raise HTTPException(404, "restaurant not found")
    
    city = await db_get_city_by_id(db, body.city)
    if not city:
        raise HTTPException(404, "city not found")

    restaurant.title = body.title
    restaurant.phone = body.phone
    restaurant.address = body.address
    restaurant.latlon = body.latlon
    restaurant.hours = body.hours
    restaurant.position = body.position
    restaurant.city = body.city
    restaurant.status = body.status
    await db.commit()

    return {"message": "restaurant updated"}

@router.delete("/")
async def delete_restaurant(
    id: int,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_restaurant_by_id(db, id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    await db_delete_restaurant(db, row)

    key = f"restaurants/{row.id}"
    await delete_object(key)
    
    return {"message": "restaurant deleted"}
