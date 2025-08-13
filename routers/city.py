from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import BaseModel, SessionDep
from db.city import (
    City,
    db_get_city_by_id,
    db_add_city,
    db_delete_city,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

class CitySchema(BaseModel):
    name: str

@router.post("/")
async def add_city(
    body: CitySchema, 
    db: SessionDep,
):
    city = City(name=body.name)
    await db_add_city(db, city)

    return {"message": "city added"}

@router.put("/")
async def edit_city(
    id: int,
    body: CitySchema,
    db: SessionDep,
):
    row = await db_get_city_by_id(db, id)
    if not row:
        raise HTTPException(404, "city not found")

    row.name = body.name
    await db.commit()

    return {"message": "city updated"}

@router.delete("/")
async def delete_city(
    id: int,
    db: SessionDep,
):
    row = await db_get_city_by_id(db, id)
    if not row:
        raise HTTPException(404, "city not found")
    
    await db_delete_city(db, row)
    
    return {"message": "city deleted"}
