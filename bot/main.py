from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel
from core.config import settings

import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()
broker = RabbitBroker(url=settings.rabbit_url)

class MessageSchema(BaseModel):
    chat_id: int
    code: str

class ContactSchema(BaseModel):
    id: int
    phone: str

@broker.subscriber("codes")
async def handle_codes(message: MessageSchema):
    await bot.send_message(
        chat_id=message.chat_id,
        text=message.code,
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Send contact",
        reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="Send contact",
                        request_contact=True,
                    ),
                ],
            ],
        ),
    )

@router.message()
async def handle_contact(message: Message):
    if message.contact.user_id == message.from_user.id:
        contact = ContactSchema(
            id=message.from_user.id,
            phone=message.contact.phone_number,
        )
        await broker.publish(
            contact.model_dump(),
            queue="contacts",
        )
        await message.answer(
            text="Wait code",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.delete()

async def main():
    dp.include_router(router)

    async with broker:
        await broker.start()
        await dp.start_polling(bot)
        logging.info("Starting Telegram bot")
    logging.info("Telegram bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
