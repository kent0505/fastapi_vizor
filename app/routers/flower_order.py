from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles, UserDep
from core.utils import get_timestamp
from db import SessionDep, BaseModel, select
from db.flower import Flower
from db.flower_order import FlowerOrder, FlowerOrderStatus

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

class FlowerOrderSchema(BaseModel):
    fid: int
    lat: str
    lon: str

@router.post("/")
async def add_flower_order(
    body: FlowerOrderSchema,
    uid: UserDep,
    db: SessionDep,
):
    flower = await db.scalar(select(Flower).filter_by(id=body.fid))
    if not flower:
        raise HTTPException(404, "flower not found")

    order = FlowerOrder(
        uid=uid,
        fid=body.fid,
        lat=body.lat,
        lon=body.lon,
        date=get_timestamp(),
        status=FlowerOrderStatus.active.value,
    )
    db.add(order)
    await db.commit()

    return {"message": "flower order added"}

@router.delete("/")
async def cancel_flower_order(
    id,
    db: SessionDep,
):
    order = await db.scalar(select(FlowerOrder).filter_by(id=id))
    if not order:
        raise HTTPException(404, "flower order not found")

    db.delete(order)
    await db.commit()

    return {"message": "flower order deleted"}

# @router.put("/")
# async def edit_flower(
#     id: int,
#     body: FlowerSchema,
#     db: SessionDep,
# ):
#     flower = await db.scalar(select(Flower).filter_by(id=id))
#     if not flower:
#         raise HTTPException(404, "flower not found")

#     flower.title = body.title
#     flower.price = body.price
#     await db.commit()

#     return {"message": "flower updated"}

# @router.patch("/photo")
# async def edit_flower_photo(
#     id: int, 
#     db: SessionDep,
#     file: UploadFile = File(),
# ):
#     flower = await db.scalar(select(Flower).filter_by(id=id))
#     if not flower:
#         raise HTTPException(404, "flower not found")

#     key = f"flowers/{id}"

#     photo = await s3_service.put_object(key, file)

#     flower.photo = photo
#     await db.commit()

#     return {
#         "message": "flower photo added",
#         "photo": photo,
#     }

# @router.delete("/")
# async def delete_flower(
#     id: int,
#     db: SessionDep,
# ):
#     flower = await db.scalar(select(Flower).filter_by(id=id))
#     if not flower:
#         raise HTTPException(404, "flower not found")

#     await db.delete(flower)
#     await db.commit()

#     return {"message": "flower deleted"}
