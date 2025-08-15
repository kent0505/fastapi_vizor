from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from faststream.rabbit import RabbitBroker

import logging
import asyncio
import os

bot = Bot(token=os.getenv("TOKEN", ""))
dp = Dispatcher()
router = Router()
broker = RabbitBroker(url=os.getenv("RABBIT_URL", ""))

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Send my contact",
                    request_contact=True,
                )
            ]
        ]
    )

    await message.answer(
        text="Send contact",
        reply_markup=keyboard,
    )

@router.message()
async def handle_contact(message: Message):
    contact = message.contact
    if contact.user_id == message.from_user.id:
        print(f"user phone: {message.contact.phone_number}")
    else:
        print(f"error: {message.contact.phone_number}")

@broker.subscriber("orders")
async def handle_orders(data: str):
    await bot.send_message(
        chat_id=1093286245,
        text=data,
    )

async def main():
    dp.include_router(router)

    async with broker:
        await broker.start()
        logging.info("Starting Telegram bot")
        await dp.start_polling(bot)
    logging.info("Telegram bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
