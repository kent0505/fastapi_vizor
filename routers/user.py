from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.security import Roles
from core.s3 import put_object
from db import AsyncSession, db_helper
from db.user import (
    UserBody,
    db_get_user_by_id,
)

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

@router.put("/")
async def edit_user(
    body: UserBody,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_user_by_id(db, body.id)
    if not row:
        raise HTTPException(404, "user not found")
    
    row.name = body.name
    row.age = body.age
    row.fcm = body.fcm
    await db.commit()

    return {"message": "user updated"}

@router.post("/")
async def add_user_photo(
    id: int, 
    file: UploadFile = File(),
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_user_by_id(db, id)
    if not row:
        raise HTTPException(404, "user not found")
    
    key = f"users/{id}"

    photo = await put_object(key, file)
    
    row.photo = photo
    await db.commit()

    return {
        "message": "user photo added",
        "photo": photo,
    }
