from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from core.config import settings
from db import db_helper
from db.user import db_get_user_by_phone

import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()

async def start_bot():
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        async with broker:
            await broker.start()
            await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

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
        # async with db_helper.session() as db:
        #     row = await db_get_user_by_phone(db, f"+{message.contact.phone_number}")
        #     if row
    else:
        print(f"error: {message.contact.phone_number}")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # startup
#     load_dotenv()
#     # logging.basicConfig(level=logging.INFO)
#     # bot_task = asyncio.create_task(start_bot())
#     logging.info("STARTUP")
#     yield
#     # shutdown
#     logging.info("SHUTDOWN")
#     # bot_task.cancel()

from faststream.rabbit import RabbitBroker

broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber("orders")
async def handle_orders(data: str):
    await bot.send_message(
        chat_id=1093286245,
        text=data,
    )
