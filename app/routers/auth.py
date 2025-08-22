from fastapi import APIRouter, HTTPException
from core.security import Roles, signJWT
from core.config import settings
from core.broker import Queue, broker
from core.utils import get_timestamp, generate_code
from db import SessionDep, BaseModel, select, db_helper
from db.user import User

router = APIRouter()

class MessageSchema(BaseModel):
    chat_id: int
    code: str

class ContactSchema(BaseModel):
    chat_id: int
    phone: str

class LoginSchema(BaseModel):
    phone: str = "+998998472580"
    code: str

@broker.subscriber(Queue.contacts.value)
async def handle_contacts(data: str):
    contact = ContactSchema.model_validate_json(data)

    async with db_helper.get_session() as db:
        user = await db.scalar(select(User).filter_by(phone=contact.phone))

        code = str(generate_code())

        if user:
            user.code = code
        else:
            admin = await db.scalar(select(User).filter_by(role=Roles.admin.value))

            if admin:
                user = User(
                    phone=contact.phone,
                    role=Roles.user.value,
                    code=code,
                    chat_id=contact.chat_id,
                )
            else:
                user = User(
                    name="Admin",
                    phone=contact.phone,
                    role=Roles.admin.value,
                    code=code,
                    chat_id=contact.chat_id,
                )

            db.add(user)

        await db.commit()

        message = MessageSchema(
            chat_id=contact.chat_id,
            code=code,
        )
        await broker.publish(
            message.model_dump_json(),
            queue=Queue.codes.value,
        )

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
