from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.security import Roles
from core.s3 import put_object
from db import BaseModel, SessionDep
from db.user import db_get_user_by_id

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

class UserSchema(BaseModel):
    id: int
    name: str
    age: str
    fcm: str

@router.get("/")
async def get_user(
    db: SessionDep,
    id: int = Depends(JWTBearer(role=Roles.user)),
):
    user = await db_get_user_by_id(db, id)
    if not user:
        raise HTTPException(404, "user not found")

    return {
        "user": {
            "id": user.id,
            "phone": user.phone,
            "name": user.name,
            "age": user.age,
            "photo": user.photo,
        }
    }

@router.put("/")
async def edit_user(
    body: UserSchema,
    db: SessionDep,
):
    user = await db_get_user_by_id(db, body.id)
    if not user:
        raise HTTPException(404, "user not found")
    
    user.name = body.name
    user.age = body.age
    user.fcm = body.fcm
    await db.commit()

    return {"message": "user updated"}

@router.patch("/")
async def edit_user_photo(
    db: SessionDep,
    file: UploadFile = File(),
    id: int = Depends(JWTBearer(role=Roles.user)),
):
    user = await db_get_user_by_id(db, id)
    if not user:
        raise HTTPException(404, "user not found")
    
    key = f"users/{id}"

    photo = await put_object(key, file)
    
    user.photo = photo
    await db.commit()

    return {
        "message": "user photo added",
        "photo": photo,
    }
