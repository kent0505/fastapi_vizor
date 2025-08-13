from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import Roles, signJWT
from core.config import settings
from core.sms import send_sms
from core.utils import get_timestamp, generate_code
from db import BaseModel, SessionDep
from db.user import (
    User,
    db_get_user_by_phone,
    db_add_user,
)

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

    row = await db_get_user_by_phone(db, body.phone)

    if row:
        row.code = code
        await db.commit()
    else:
        await db_add_user(
            db,
            user=User(
                phone=body.phone,
                code=code,
                role=Roles.user,
            )
        )

    return {"message": "sms code sent"}

@router.post("/login")
async def login(
    body: LoginSchema,
    db: SessionDep,
):
    row = await db_get_user_by_phone(db, body.phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    if row.code is None:
        raise HTTPException(400, "verification code not sent")

    if row.code != body.code:
        raise HTTPException(400, "verification code is incorrect")

    row.code = None
    await db.commit()

    access_token: str = signJWT(
        row.id, 
        row.role, 
        get_timestamp() + settings.year_seconds,
    )

    return {
        "access_token": access_token,
        "role": row.role,
    }
