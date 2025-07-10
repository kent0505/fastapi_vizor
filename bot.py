from aiogram         import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types   import Message
from settings        import settings

import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()

async def start_bot():
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello")
