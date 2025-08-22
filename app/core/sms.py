from fastapi import HTTPException
from twilio.rest import Client
from core.config import settings

import logging

class SmsService:
    def __init__(self):
        self.client = Client(
            settings.account_sid,
            settings.auth_token,
        )

    async def send_sms(
        self, 
        to: str, 
        body: str,
    ):
        try:
            message = self.client.messages.create(
                to=to,
                body=body,
            )
            logging.info(message.sid)
        except Exception as e:
            raise HTTPException(500, str(e))

sms_service = SmsService()
