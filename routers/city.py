from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db.city import (
    City,
    db_get_city_by_id,
    db_add_city,
    db_update_city,
    db_delete_city,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_city(body: City):
    await db_add_city(body)

    return {"message": "city added"}

@router.put("/")
async def edit_city(body: City):
    row = await db_get_city_by_id(body.id)
    if not row:
        raise HTTPException(404, "city not found")

    await db_update_city(body)

    return {"message": "city updated"}

@router.delete("/")
async def delete_city(id: int):
    row = await db_get_city_by_id(id)
    if not row:
        raise HTTPException(404, "city not found")
    
    await db_delete_city(id)
    
    return {"message": "city deleted"}
