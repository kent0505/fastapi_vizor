from fastapi import APIRouter, HTTPException
from core.security import Roles, signJWT
from core.config import settings
from core.sms import send_sms
from core.utils import get_timestamp, generate_code
from db import SessionDep, BaseModel, select
from db.user import User

router = APIRouter()

class PhoneSchema(BaseModel):
    phone: str = "+998998472580"

class LoginSchema(BaseModel):
    phone: str = "+998998472580"
    code: str

@router.post("/send_code")
async def send_code(
    body: PhoneSchema,
    db: SessionDep,
):
    code = str(generate_code())

    await send_sms(code, body.phone)

    user = await db.scalar(select(User).filter_by(phone=body.phone))

    if user:
        user.code = code
        await db.commit()
    else:
        user = User(
            phone=body.phone,
            code=code,
            role=Roles.user.value,
        )
        db.add(user)
        await db.commit()

    return {"message": "sms code sent"}

@router.post("/login")
async def login(
    body: LoginSchema,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(phone=body.phone))

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
