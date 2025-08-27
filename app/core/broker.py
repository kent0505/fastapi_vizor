from faststream.rabbit import RabbitBroker
from faststream.rabbit.fastapi import RabbitRouter
from pydantic import BaseModel
from enum import Enum
from core.config import settings
from db import db_helper, select
from db.user import User

class Queue(str, Enum):
    contacts = "contacts"
    codes = "codes"

class ContactSchema(BaseModel):
    phone: str

broker = RabbitBroker(url=settings.rabbit_url)

router = RabbitRouter(url=settings.rabbit_url)

@router.post("/contact")
async def test(contact: ContactSchema):
    await router.broker.publish(
        contact.model_dump_json(),
        queue=Queue.contacts.value,
    )
    return {"message": "OK"}

@broker.subscriber(Queue.contacts.value)
async def handle_contacts(data: str):
    contact = ContactSchema.model_validate_json(data)

    async with db_helper.get_session() as db:
        user = await db.scalar(select(User).filter_by(phone=contact.phone))
        if user:
            user.phone = contact.phone
            await db.commit()
