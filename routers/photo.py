from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import put_object, delete_object
from db.restaurant import db_get_restaurant_by_id
from db import AsyncSession, db_helper

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/restaurant")
async def add_restaurant_photo(
    id: int, 
    file: UploadFile = File(),
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_restaurant_by_id(db, id)
    if not row:
        raise HTTPException(404, "restaurant not found")
    
    key = f"restaurants/{id}"

    photo = await put_object(key, file)

    row.photo = photo
    await db.commit()

    return {
        "message": "restaurant photo added",
        "photo": photo,
    }

@router.delete("/")
async def delete_photo(key: str):
    await delete_object(key)

    return {"message": "photo deleted"}
