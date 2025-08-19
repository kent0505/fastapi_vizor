from faststream.rabbit import RabbitBroker
from core.config import settings

import httpx
import logging
import os

broker = RabbitBroker(url=settings.rabbit_url)
token = os.getenv("TOKEN")

@broker.subscriber("messages")
async def handle_messages(message: dict):
    async with httpx.AsyncClient() as client:
        try:
            if not token:
                raise ValueError("TOKEN environment variable is required")

            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": 1093286245,
                    "text": message["text"],
                }
            )

            resp.raise_for_status()

            return resp.json()
        except Exception as e:
            logging.error(e)
            return {"message": f"{e}"}
