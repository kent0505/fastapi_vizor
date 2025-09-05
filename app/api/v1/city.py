from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, select
from db.city import City, CitySchema

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_city(
    body: CitySchema, 
    db: SessionDep,
):
    city = await db.scalar(select(City).filter_by(name=body.name))
    if city:
        raise HTTPException(409, "city already exists")

    city = City(name=body.name)
    db.add(city)
    await db.commit()

    return {"message": "city added"}

@router.put("/")
async def edit_city(
    id: int,
    body: CitySchema,
    db: SessionDep,
):
    city = await db.scalar(select(City).filter_by(id=id))
    if not city:
        raise HTTPException(404, "city not found")

    city.name = body.name
    await db.commit()

    return {"message": "city updated"}

@router.patch("/position")
async def edit_city_position(
    id: int,
    position: int,
    db: SessionDep,
):
    city = await db.scalar(select(City).filter_by(id=id))
    if not city:
        raise HTTPException(404, "city not found")

    city.position = position
    await db.commit()

    return {"message": "city position updated"}

@router.delete("/")
async def delete_city(
    id: int,
    db: SessionDep,
):
    city = await db.scalar(select(City).filter_by(id=id))
    if not city:
        raise HTTPException(404, "city not found")

    await db.delete(city)
    await db.commit()
    
    return {"message": "city deleted"}
