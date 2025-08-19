from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.utils import get_timestamp
from core.s3 import put_object, delete_object
from db import SessionDep, BaseModel, select
from db.restaurant import Restaurant
from db.panorama import Panorama

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
    restaurant = await db.scalar(select(Restaurant).filter_by(id=rid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    key = f"panoramas/{get_timestamp()}"

    photo = await put_object(key, file)

    panorama = Panorama(
        rid=rid,
        photo=photo,
    )
    db.add(panorama)
    await db.commit()

    return {"message": "panorama added"}

@router.patch("/")
async def edit_panorama_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    panorama = await db.scalar(select(Panorama).filter_by(id=id))
    if not panorama:
        raise HTTPException(404, "panorama not found")

    key = f"panoramas/{id}"

    photo = await put_object(key, file)

    panorama.photo = photo
    await db.commit()

    return {
        "message": "panorama photo added",
        "photo": photo,
    }

@router.delete("/")
async def delete_panorama(
    id: int,
    db: SessionDep,
):
    panorama = await db.scalar(select(Panorama).filter_by(id=id))
    if not panorama:
        raise HTTPException(404, "panorama not found")

    await delete_object(panorama.photo)

    await db.delete(panorama)
    await db.commit()

    return {"message": "panorama deleted"}
