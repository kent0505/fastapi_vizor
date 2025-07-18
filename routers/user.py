from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles, signJWT
from core.schemas import User
from core.utils import get_timestamp, get_format
from core.settings import settings, s3
from core.db import (
    db_get_user_by_id, 
    db_get_user_by_phone,
    db_add_user,
    db_update_user,
    db_update_user_photo,
    db_delete_user,
)

router = APIRouter()

@router.post("/login")
async def login(phone: str, password: str):
    row = await db_get_user_by_phone(phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    now = get_timestamp()
    role = Roles.user
    exp = now + settings.year_seconds
    if password == settings.password:
        role = Roles.admin
        exp = now + settings.day_seconds

    access_token: str = signJWT(row.id, role, exp)

    return {
        "access_token": access_token,
        "role": role,
    }

@router.post("/register")
async def register(body: User):
    row = await db_get_user_by_phone(body.phone)
    if row:
        raise HTTPException(404, "user already exists")

    await db_add_user(body)

    return {"message": "user registered"}

@router.put("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def edit_user(body: User):
    row = await db_get_user_by_id(body.id)
    if not row:
        raise HTTPException(404, "user not found")
    
    if row.phone != body.phone:
        row = await db_get_user_by_phone(body.phone)
        if row:
            raise HTTPException(404, "phone number already exists")

    await db_update_user(body)

    return {"message": "user updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_user(id: int):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")
    
    s3.delete_object(
        Bucket=settings.bucket, 
        Key=f"users/{id}.{get_format(row.photo)}",
    )

    await db_delete_user(id)

    return {"message": "user deleted"}

@router.put("/photo", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def edit_user_photo(id: int, file: UploadFile = File(...)):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")
    
    format = get_format(str(file.filename))
    if format not in settings.image_formats:
        raise HTTPException(400, 'file error')

    key = f"users/{id}.{format}"
    url = f"{settings.endpoint_url}/{settings.bucket}/{key}"

    s3.delete_object(
        Bucket=settings.bucket, 
        Key=f"users/{id}.{get_format(row.photo)}",
    )

    s3.put_object(
        Bucket=settings.bucket,
        Key=key,
        Body=await file.read(),
        ContentType=file.content_type,
    )

    await db_update_user_photo(url, id)

    return {"message": "user photo updated"}
