from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.s3 import delete_object
from db.city import db_get_city_by_id
from db.restaurant import (
    Restaurant,
    db_get_restaurant_by_id,
    db_add_restaurant,
    db_update_restaurant,
    db_delete_restaurant,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_restaurant(body: Restaurant):
    row = await db_get_city_by_id(body.city)
    if not row:
        raise HTTPException(404, "city not found")

    await db_add_restaurant(body)

    return {"message": "restaurant added"}

@router.put("/")
async def edit_restaurant(body: Restaurant):
    row = await db_get_restaurant_by_id(body.id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    row = await db_get_city_by_id(body.city)
    if not row:
        raise HTTPException(404, "city not found")

    await db_update_restaurant(body)

    return {"message": "restaurant updated"}

@router.delete("/")
async def delete_restaurant(id: int):
    row = await db_get_restaurant_by_id(id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    await db_delete_restaurant(id)

    key = f"restaurants/{row.id}"
    await delete_object(key)
    
    return {"message": "restaurant deleted"}
