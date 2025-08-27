from fastapi import APIRouter, HTTPException
from core.security import Roles, signJWT
from core.config import settings
from core.utils import get_timestamp, generate_code
from core.sms import sms_service
from db import SessionDep, BaseModel, select
from db.user import User

router = APIRouter()

class AdminSchema(BaseModel):
    name: str = "Otabek"
    phone: str = "+998998472580"

class PhoneSchema(BaseModel):
    phone: str = "+998998472580"

class LoginSchema(BaseModel):
    phone: str = "+998998472580"
    code: str

@router.post("/admin")
async def create_admin(
    body: AdminSchema,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(role=Roles.admin.value))
    if user:
        raise HTTPException(400, "admin exists")

    user = User(
        name=body.name,
        phone=body.phone,
        role=Roles.admin.value,
    )
    db.add(user)
    await db.commit()

    return {"message": "admin created"}

@router.post("/send_code")
async def send_code(
    body: PhoneSchema,
    db: SessionDep,
):
    code = str(generate_code())

    # await sms_service.send_sms(body.phone, code)

    user = await db.scalar(select(User).filter_by(phone=body.phone))

    if user:
        user.code = code
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
