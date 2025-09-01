from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.security import Roles, UserDep
from core.s3 import s3_service
from db import SessionDep, select
from db.user import User, UserEditSchema

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

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
            "id": id,
            "phone": user.phone,
            "name": user.name,
            "age": user.age,
            "role": user.role,
            "photo": user.photo,
        }
    }

@router.put("/")
async def edit_user(
    id: UserDep,
    body: UserEditSchema,
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

@router.patch("/photo")
async def edit_user_photo(
    id: UserDep,
    db: SessionDep,
    file: UploadFile = File(),
):
    user = await db.scalar(select(User).filter_by(id=id))
    if not user:
        raise HTTPException(404, "user not found")

    key = f"users/{id}"

    photo = await s3_service.put_object(key, file)

    user.photo = photo
    await db.commit()

    return {
        "message": "user photo added",
        "photo": photo,
    }
