from faststream.rabbit import RabbitBroker
from enum import Enum
from core.config import settings

class Queue(str, Enum):
    contacts = "contacts"
    codes = "codes"

broker = RabbitBroker(url=settings.rabbit_url)
