from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from core.settings import settings

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
    await message.answer(text=str(message.chat.id))

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

# from faststream.rabbit import RabbitBroker

# broker = RabbitBroker(settings.rabbit_url)

# @broker.subscriber("orders")
# async def handle_orders(data: str):
#     await bot.send_message(
#         chat_id=1093286245,
#         text=data,
#     )

# async with broker:
        #     await broker.start()
        #     await dp.start_polling(bot)
