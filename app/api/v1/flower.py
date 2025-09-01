from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from db import SessionDep, select
from db.flower import Flower, FlowerSchema
from core.s3 import s3_service

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.stuff))])

@router.post("/")
async def add_flower(
    body: FlowerSchema, 
    db: SessionDep,
):
    flower = Flower(
        title=body.title,
        price=body.price,
    )
    db.add(flower)
    await db.commit()

    return {"message": "flower added"}

@router.put("/")
async def edit_flower(
    id: int,
    body: FlowerSchema,
    db: SessionDep,
):
    flower = await db.scalar(select(Flower).filter_by(id=id))
    if not flower:
        raise HTTPException(404, "flower not found")

    flower.title = body.title
    flower.price = body.price
    await db.commit()

    return {"message": "flower updated"}

@router.patch("/photo")
async def edit_flower_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    flower = await db.scalar(select(Flower).filter_by(id=id))
    if not flower:
        raise HTTPException(404, "flower not found")

    key = f"flowers/{id}"

    photo = await s3_service.put_object(key, file)

    flower.photo = photo
    await db.commit()

    return {
        "message": "flower photo added",
        "photo": photo,
    }

@router.delete("/")
async def delete_flower(
    id: int,
    db: SessionDep,
):
    flower = await db.scalar(select(Flower).filter_by(id=id))
    if not flower:
        raise HTTPException(404, "flower not found")

    await db.delete(flower)
    await db.commit()

    return {"message": "flower deleted"}
