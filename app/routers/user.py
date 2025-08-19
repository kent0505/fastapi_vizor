from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.security import Roles, UserDep
from core.s3 import put_object
from db import BaseModel, SessionDep, Optional, select
from db.user import User

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

class UserSchema(BaseModel):
    name: str
    age: str
    fcm: Optional[str] = None

@router.get("/")
async def get_user(
    id: UserDep,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(id=id))
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
    id: UserDep,
    body: UserSchema,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(id=id))
    if not user:
        raise HTTPException(404, "user not found")

    user.name = body.name
    user.age = body.age
    user.fcm = body.fcm
    await db.commit()

    return {"message": "user updated"}

@router.patch("/")
async def edit_user_photo(
    id: UserDep,
    db: SessionDep,
    file: UploadFile = File(),
):
    user = await db.scalar(select(User).filter_by(id=id))
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
