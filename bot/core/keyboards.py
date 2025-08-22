from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_contact_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="Send contact",
                request_contact=True,
            ),
        ],
    ],
)