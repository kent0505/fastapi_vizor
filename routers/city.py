from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import AsyncSession, db_helper
from db.city import (
    City,
    CityBody,
    db_get_city_by_id,
    db_add_city,
    db_delete_city,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_city(
    body: CityBody, 
    db: AsyncSession = Depends(db_helper.get_db),
):
    city = City(name=body.name)
    await db_add_city(db, city)

    return {"message": "city added"}

@router.put("/")
async def edit_city(
    body: CityBody,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_city_by_id(db, body.id)
    if not row:
        raise HTTPException(404, "city not found")

    row.name = body.name
    await db.commit()

    return {"message": "city updated"}

@router.delete("/")
async def delete_city(
    id: int,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_city_by_id(db, id)
    if not row:
        raise HTTPException(404, "city not found")
    
    await db_delete_city(db, row)
    
    return {"message": "city deleted"}
