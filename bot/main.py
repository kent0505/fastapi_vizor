from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from pydantic import BaseModel
from core.broker import Queue, broker
from core.config import settings
from core.keyboards import send_contact_button

import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()

class MessageSchema(BaseModel):
    chat_id: int
    code: str

class ContactSchema(BaseModel):
    chat_id: int
    phone: str

@broker.subscriber(Queue.codes.value)
async def handle_codes(data: str):
    message = MessageSchema.model_validate_json(data)

    await bot.send_message(
        chat_id=message.chat_id,
        text=message.code,
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Send contact",
        reply_markup=send_contact_button,
    )

@router.message()
async def handle_all(message: Message):
    if message.contact and message.contact.user_id == message.from_user.id:
        contact = ContactSchema(
            chat_id=message.from_user.id,
            phone=message.contact.phone_number,
        )
        await broker.publish(
            contact.model_dump_json(),
            queue=Queue.contacts.value,
        )
    await message.delete()

async def main():
    dp.include_router(router)
    try:
        await broker.start()
        await dp.start_polling(bot)
    except:
        await broker.stop()

if __name__ == "__main__":
    asyncio.run(main())
