from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from core.schemas import Restaurant
from core.utils import get_format
from core.settings import settings
from core.s3 import delete_object, put_object
from core.db import (
    db_get_restaurants,
    db_get_restaurant_by_id,
    db_add_restaurant,
    db_update_restaurant,
    db_delete_restaurant,
    db_update_restaurant_photo,
)

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def get_restaurants():
    rows = await db_get_restaurants()

    return {"restaurants": rows}

@router.post("/", dependencies=[Depends(JWTBearer())])
async def add_restaurant(body: Restaurant):
    await db_add_restaurant(body)

    return {"message": "restaurant added"}

@router.put("/", dependencies=[Depends(JWTBearer())])
async def edit_restaurant(body: Restaurant):
    row = await db_get_restaurant_by_id(body.id)
    if not row:
        raise HTTPException(404, "restaurant not found")

    await db_update_restaurant(body)

    return {"message": "restaurant updated"}

@router.patch("/", dependencies=[Depends(JWTBearer())])
async def edit_restaurant_photo(id: int, file: UploadFile = File()):
    row = await db_get_restaurant_by_id(id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    format = get_format(str(file.filename))
    if format not in settings.image_formats:
        raise HTTPException(400, 'file error')

    key = f"restaurants/{id}.{format}"
    url = f"{settings.endpoint_url}/{settings.bucket}/{key}"

    await delete_object(f"restaurants/{id}.{get_format(row.photo)}")
    await put_object(key, file)

    await db_update_restaurant_photo(url, id)

    return {"message": "restaurant photo updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_restaurant(id: int):
    row = await db_get_restaurant_by_id(id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    await delete_object(f"restaurants/{id}.{get_format(row.photo)}")
    
    await db_delete_restaurant(id)
    
    return {"message": "restaurant deleted"}
