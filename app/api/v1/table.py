from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles
from db import SessionDep, select
from db.table import RestaurantTable, RestaurantTableSchema, TableStatus
from db.restaurant import Restaurant

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.stuff))])

@router.post("/")
async def add_table(
    body: RestaurantTableSchema, 
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=body.rid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")
    
    table = await db.scalar(select(RestaurantTable).filter_by(
        number=body.number, 
        rid=body.rid,
    ))
    if table:
        raise HTTPException(400, "table number exists")

    table = RestaurantTable(
        number=body.number,
        rid=body.rid,
    )
    db.add(table)
    await db.commit()

    return {"message": "table added"}

@router.patch("/")
async def edit_table_status(
    id: int,
    status: TableStatus,
    db: SessionDep,
):
    table = await db.scalar(select(RestaurantTable).filter_by(id=id))
    if not table:
        raise HTTPException(404, "table not found")

    table.status = status.value
    await db.commit()

    return {"message": "table status updated"}

@router.delete("/")
async def delete_table(
    id: int,
    db: SessionDep,
):
    table = await db.scalar(select(RestaurantTable).filter_by(id=id))
    if not table:
        raise HTTPException(404, "table not found")

    await db.delete(table)
    await db.commit()
    
    return {"message": "table deleted"}
