from faststream.rabbit.fastapi import RabbitRouter
from pydantic import BaseModel
from core.config import settings

router = RabbitRouter(url=settings.rabbit_url)

class MessageSchema(BaseModel):
    id: int
    text: str

@router.post("/message")
async def test(message: MessageSchema):
    await router.broker.publish(
        message.model_dump(),
        queue="messages",
    )
    return {"message": "OK"}
