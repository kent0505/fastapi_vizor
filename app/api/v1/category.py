from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, select
from db.category import Category, CategorySchema

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/")
async def add_category(
    body: CategorySchema, 
    db: SessionDep,
):
    category = Category(name=body.name)
    db.add(category)
    await db.commit()

    return {"message": "category added"}

@router.put("/")
async def edit_category(
    id: int,
    body: CategorySchema,
    db: SessionDep,
):
    category = await db.scalar(select(Category).filter_by(id=id))
    if not category:
        raise HTTPException(404, "category not found")

    category.name = body.name
    await db.commit()

    return {"message": "category updated"}

@router.delete("/")
async def delete_category(
    id: int,
    db: SessionDep,
):
    category = await db.scalar(select(Category).filter_by(id=id))
    if not category:
        raise HTTPException(404, "category not found")

    await db.delete(category)
    await db.commit()

    return {"message": "category deleted"}
