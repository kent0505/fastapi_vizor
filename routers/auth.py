from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import Roles, signJWT
from core.config import settings
from core.sms import send_sms
from core.utils import get_timestamp, generate_code
from db import SessionDep, BaseModel
from db.user import User, db_get_user_by_phone

router = APIRouter()

class PhoneSchema(BaseModel):
    phone: str

class LoginSchema(BaseModel):
    phone: str
    code: str

@router.post("/send_code")
async def send_code(
    body: PhoneSchema,
    db: SessionDep,
):
    code = str(generate_code())

    await send_sms(code, body.phone)

    user = await db_get_user_by_phone(db, body.phone)

    if user:
        user.code = code
        await db.commit()
    else:
        user = User(
            phone=body.phone,
            code=code,
            role=Roles.user,
        )
        db.add(user)
        await db.commit()

    return {"message": "sms code sent"}

@router.post("/login")
async def login(
    body: LoginSchema,
    db: SessionDep,
):
    user = await db_get_user_by_phone(db, body.phone)
    if not user:
        raise HTTPException(404, "phone number does not exist")

    if user.code is None:
        raise HTTPException(400, "verification code not sent")

    if user.code != body.code:
        raise HTTPException(400, "verification code is incorrect")

    user.code = None
    await db.commit()

    access_token: str = signJWT(
        user.id, 
        user.role, 
        get_timestamp() + settings.year_seconds,
    )

    return {
        "access_token": access_token,
        "role": user.role,
    }
