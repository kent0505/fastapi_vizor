from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import put_object, delete_object
from db import SessionDep, BaseModel, Optional, select
from db.city import City
from db.restaurant import Restaurant

router = APIRouter(dependencies=[Depends(JWTBearer())])

class RestaurantSchema(BaseModel):
    title: str
    phone: str
    address: str
    latlon: str
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
        latlon=body.latlon,
        hours=body.hours,
        city=body.city,
        position=body.position,
        status=body.status,   
    )
    db.add(restaurant)
    await db.commit()

    return {"message": "restaurant added"}

@router.put("/")
async def edit_restaurant(
    id: int,
    body: RestaurantSchema,
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
    restaurant.latlon = body.latlon
    restaurant.hours = body.hours
    restaurant.city = body.city
    restaurant.position = body.position
    restaurant.status = body.status
    await db.commit()

    return {"message": "restaurant updated"}

@router.patch("/restaurant")
async def edit_restaurant_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    key = f"restaurants/{id}"

    photo = await put_object(key, file)

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
    await delete_object(key)

    await db.delete(restaurant)
    await db.commit()

    return {"message": "restaurant deleted"}
