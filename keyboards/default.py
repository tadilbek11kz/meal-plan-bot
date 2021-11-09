from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Get data"),
        ],
        [
            KeyboardButton(text="Subscription"),
            KeyboardButton(text="Settings")
        ]
    ],
    resize_keyboard=True
)
