from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.utils import get_timestamp
from core.s3 import put_object, delete_object
from db import SessionDep, BaseModel
from db.restaurant import db_get_restaurant_by_id
from db.panorama import (
    Panorama, 
    db_get_panorama_by_id, 
    db_add_panorama,
    db_delete_panorama,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

class PanoramaSchema(BaseModel):
    rid: int
    photo: str

@router.post("/")
async def add_panorama(
    rid: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    row = await db_get_restaurant_by_id(db, rid)
    if not row:
        raise HTTPException(404, "restaurant not found")

    key = f"panoramas/{get_timestamp()}"

    photo = await put_object(key, file)

    panorama = Panorama(
        rid=rid,
        photo=photo,
    )
    await db_add_panorama(db, panorama)

    return {"message": "panorama added"}

@router.delete("/")
async def delete_panorama(
    id: int,
    db: SessionDep,
):
    row = await db_get_panorama_by_id(db, id)
    if not row:
        raise HTTPException(404, "panorama not found")

    await delete_object(row.photo)

    await db_delete_panorama(db, row)

    return {"message": "panorama deleted"}
