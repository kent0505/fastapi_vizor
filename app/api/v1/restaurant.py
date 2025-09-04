from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import s3_service
from db import SessionDep, select
from db.city import City
from db.restaurant import Restaurant, RestaurantSchema, RestaurantStatus

router = APIRouter(dependencies=[Depends(JWTBearer())])

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
    restaurant.lat = body.lat
    restaurant.lon = body.lon
    restaurant.hours = body.hours
    restaurant.city = body.city
    await db.commit()

    return {"message": "restaurant updated"}

@router.patch("/position")
async def edit_restaurant_position(
    id: int, 
    position: int,
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    restaurant.position = position
    await db.commit()

    return {"message": "restaurant position updated"}

@router.patch("/status")
async def edit_restaurant_status(
    id: int, 
    status: RestaurantStatus,
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    restaurant.status = status.value
    await db.commit()

    return {"message": "restaurant status updated"}

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

    await s3_service.delete_object(restaurant.photo)

    await db.delete(restaurant)
    await db.commit()

    return {"message": "restaurant deleted"}
