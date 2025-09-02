from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles, UserDep
from core.utils import get_timestamp
from db import SessionDep, select
from db.flower import Flower
from db.flower_order import FlowerOrder, FlowerOrderSchema

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

@router.get("/")
async def get_flower_orders(
    uid: UserDep,
    db: SessionDep,
):
    orders = (await db.scalars(select(FlowerOrder).filter_by(uid=uid))).all()

    return {"orders": orders}

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
        note=body.note,
        date=get_timestamp(),
    )
    db.add(order)
    await db.commit()

    return {"message": "flower order added"}

@router.delete("/")
async def cancel_flower_order(
    id: int,
    db: SessionDep,
):
    order = await db.scalar(select(FlowerOrder).filter_by(id=id))
    if not order:
        raise HTTPException(404, "flower order not found")

    await db.delete(order)
    await db.commit()

    return {"message": "flower order deleted"}
