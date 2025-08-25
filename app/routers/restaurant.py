from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import Optional
from core.security import JWTBearer
from core.s3 import s3_service
from db import SessionDep, BaseModel, select
from db.city import City
from db.restaurant import Restaurant

router = APIRouter(dependencies=[Depends(JWTBearer())])

class RestaurantSchema(BaseModel):
    title: str
    phone: str
    address: str
    lat: str
    lon: str
    hours: str
    city: int

class RestaurantUpdateSchema(BaseModel):
    title: str
    phone: str
    address: str
    lat: str
    lon: str
    hours: str
    city: int
    position: Optional[int] = None
    status: Optional[int] = None

@router.post("/")
async def add_restaurant(
    body: RestaurantSchema,
    db: SessionDep,
):
    city = await db.scalar(select(City).filter_by(id=body.city))
    if not city:
        raise HTTPException(404, "city not found")

    restaurant = Restaurant(
        title=body.title,
        phone=body.phone,
        address=body.address,
        lat=body.lat,
        lon=body.lon,
        hours=body.hours,
        city=body.city,  
    )
    db.add(restaurant)
    await db.commit()

    return {"message": "restaurant added"}

@router.put("/")
async def edit_restaurant(
    id: int,
    body: RestaurantUpdateSchema,
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    city = await db.scalar(select(City).filter_by(id=body.city))
    if not city:
        raise HTTPException(404, "city not found")

    restaurant.title = body.title
    restaurant.phone = body.phone
    restaurant.address = body.address
    restaurant.lat = body.lat
    restaurant.lon = body.lon
    restaurant.hours = body.hours
    restaurant.city = body.city
    restaurant.position = body.position
    restaurant.status = body.status
    await db.commit()

    return {"message": "restaurant updated"}

@router.patch("/photo")
async def edit_restaurant_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    key = f"restaurants/{id}"

    photo = await s3_service.put_object(key, file)

    restaurant.photo = photo
    await db.commit()

    return {
        "message": "restaurant photo added",
        "photo": photo,
    }

@router.delete("/")
async def delete_restaurant(
    id: int,
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    key = f"restaurants/{restaurant.id}"
    await s3_service.delete_object(key)

    await db.delete(restaurant)
    await db.commit()

    return {"message": "restaurant deleted"}
