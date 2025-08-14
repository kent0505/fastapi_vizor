from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, BaseModel
from db.category import Category, db_get_category_by_id

router = APIRouter(dependencies=[Depends(JWTBearer())])

class CategorySchema(BaseModel):
    name: str

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
    category = await db_get_category_by_id(db, id)
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
    category = await db_get_category_by_id(db, id)
    if not category:
        raise HTTPException(404, "category not found")

    await db.delete(category)
    await db.commit()

    return {"message": "category deleted"}
