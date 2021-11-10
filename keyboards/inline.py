from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import subscription_callback, get_data_callback, image_callback


money_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Campus Cash",
                                 callback_data=get_data_callback.new(type=8)),
            InlineKeyboardButton(text="Campus Dirhams",
                                 callback_data=get_data_callback.new(type=50))
        ],
        [
            InlineKeyboardButton(text="Falcon Dirhams",
                                 callback_data=get_data_callback.new(type=51)),
            InlineKeyboardButton(text="Flex Dirhams",
                                 callback_data=get_data_callback.new(type=71))
        ],
        [
            InlineKeyboardButton(text="Meal Swipes",
                                 callback_data=get_data_callback.new(type=48))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

subscription_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Subscribe!",
                                 callback_data=subscription_callback.new(command="subscribe")),
            InlineKeyboardButton(text="Unsubscribe :(",
                                 callback_data=subscription_callback.new(command="unsubscribe"))
        ],
        [
            InlineKeyboardButton(text="Created by: Adilbek",
                                 url="https://tadilbek11kz.github.io")
        ]
    ],
    resize_keyboard=True
)

greet_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Created by: Adilbek",
                                 url="https://tadilbek11kz.github.io")
        ]
    ],
    resize_keyboard=True
)


def settings_menu(user):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Rows: {user["rows"]}', url="https://tadilbek11kz.github.io"),
                InlineKeyboardButton(
                    text=f'Image: {user["image"]}', callback_data=image_callback.new(user["image"]))
            ],
            [
                InlineKeyboardButton(
                    text=f'Login: {user["login"]}', url="https://tadilbek11kz.github.io"),
            ]
        ],
        resize_keyboard=True
    )