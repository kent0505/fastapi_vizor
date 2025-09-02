from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import s3_service
from db import SessionDep, select
from db.restaurant import Restaurant
from db.panorama import Panorama

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_panorama(
    rid: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=rid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")
    
    panorama = Panorama(rid=rid)
    db.add(panorama)
    await db.commit()
    await db.refresh(panorama)

    key = f"panoramas/{panorama.id}"

    photo = await s3_service.put_object(key, file)

    panorama.photo = photo
    await db.commit()

    return {"message": "panorama added"}

@router.patch("/photo")
async def edit_panorama_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    panorama = await db.scalar(select(Panorama).filter_by(id=id))
    if not panorama:
        raise HTTPException(404, "panorama not found")

    key = f"panoramas/{id}"

    photo = await s3_service.put_object(key, file)

    panorama.photo = photo
    await db.commit()

    return {
        "message": "panorama photo updated",
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

    await s3_service.delete_object(panorama.photo)

    await db.delete(panorama)
    await db.commit()

    return {"message": "panorama deleted"}
