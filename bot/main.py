from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from faststream.rabbit import RabbitBroker
from config import settings

import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()
broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber("orders")
async def handle_orders(data: str):
    await bot.send_message(
        chat_id=1093286245,
        text=data,
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text="Send contact",
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

async def main():
    dp.include_router(router)

    async with broker:
        await broker.start()
        await dp.start_polling(bot)
        logging.info("Starting Telegram bot")
    logging.info("Telegram bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
