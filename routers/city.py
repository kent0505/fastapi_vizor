from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, BaseModel, select
from db.city import City

router = APIRouter(dependencies=[Depends(JWTBearer())])

class CitySchema(BaseModel):
    name: str

@router.post("/")
async def add_city(
    body: CitySchema, 
    db: SessionDep,
):
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
