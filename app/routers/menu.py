from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import s3_service
from db import SessionDep, BaseModel, select
from db.restaurant import Restaurant
from db.category import Category
from db.menu import Menu

router = APIRouter(dependencies=[Depends(JWTBearer())])

class MenuSchema(BaseModel):
    title: str
    description: str
    price: str
    currency: str
    cid: int
    rid: int

@router.post("/")
async def add_menu(
    body: MenuSchema,
    db: SessionDep,
):
    category = await db.scalar(select(Category).filter_by(id=body.cid))
    if not category:
        raise HTTPException(404, "category not found")

    restaurant = await db.scalar(select(Restaurant).filter_by(id=body.rid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    menu = Menu(
        title=body.title,
        description=body.description,
        price=body.price,
        currency=body.currency,
        cid=body.cid,
        rid=body.rid,
    )
    db.add(menu)
    await db.commit()

    return {"message": "menu added"}

@router.put("/")
async def edit_menu(
    id: int,
    body: MenuSchema,
    db: SessionDep,
):
    menu = await db.scalar(select(Menu).filter_by(id=id))
    if not menu:
        raise HTTPException(404, "menu not found")

    category = await db.scalar(select(Category).filter_by(id=body.cid))
    if not category:
        raise HTTPException(404, "category not found")

    restaurant = await db.scalar(select(Restaurant).filter_by(id=body.rid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    menu.title=body.title,
    menu.description=body.description,
    menu.price=body.price,
    menu.currency=body.currency,
    menu.cid=body.cid,
    menu.rid=body.rid,
    await db.commit()

    return {"message": "menu updated"}

@router.patch("/")
async def edit_menu_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    menu = await db.scalar(select(Menu).filter_by(id=id))
    if not menu:
        raise HTTPException(404, "menu not found")

    key = f"menus/{id}"

    photo =  await s3_service.put_object(key, file)

    menu.photo = photo
    await db.commit()

    return {"message": "menu photo updated"}

@router.delete("/")
async def delete_menu(
    id: int,
    db: SessionDep,
):
    menu = await db.scalar(select(Menu).filter_by(id=id))
    if not menu:
        raise HTTPException(404, "menu not found")

    key = f"menus/{menu.id}"
    await s3_service.delete_object(key)

    await db.delete(menu)
    await db.commit()

    return {"message": "menu deleted"}
