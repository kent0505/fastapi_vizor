from twilio.rest import Client
from core.config import settings

import logging

client = Client(
    settings.account_sid, 
    settings.auth_token,
)

async def send_sms(
    body: str,
    to: str,
):
    try:
        message = client.messages.create(
            body=body, 
            to=to,
        )
        logging.info(message)
    except Exception as e:
        logging.error(e)
