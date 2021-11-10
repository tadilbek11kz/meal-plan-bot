
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from keyboards.default import menu
from keyboards.inline import subscription_menu, greet_menu, money_menu, settings_menu
from callbacks import subscription_callback, get_data_callback, image_callback

from data import data
from database import DataBase
from config import TELEGRAM_TOKEN, MONGO_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Init Database (Mongo)
db = DataBase(MONGO_TOKEN)


@dp.message_handler(commands=["admin"])
async def admin_message(message: types.Message):
    print(message.from_user.id)
    if (message.from_user.id == 364527781):
        subscirptions = list(db.get_subscriptions())
        for user in subscirptions:
            await bot.send_message(user["user_id"], text="".join(message.text.split("/admin")))


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # if user do not exist add user to db
        db.add_subscriber(message.from_user.id)
    else:
        # if user exist, update status
        db.update_subscription(message.from_user.id, True)
    await message.answer("NYUAD Money Bot – real time data about your NYU banking account", reply_markup=greet_menu)
    await message.answer("By clicking on the «Get data» button, you will be able to receive up-to-date information on your bank account. By subscribing to the Bot, you will receive notifications about every transaction on your account", reply_markup=menu)


@dp.message_handler(Text(equals="Subscription"))
async def subscription(message: types.Message):
    await message.answer(f'Notifications about every transaction on your account\nSubscription status: {db.subscriber_status(message.from_user.id)}', reply_markup=subscription_menu)


@dp.message_handler(Text(equals="Get data"))
async def get_data(message: types.Message):
    await message.answer("Choose type of data you want to recieve", reply_markup=money_menu)


@dp.message_handler(Text(equals="Settings"))
async def get_data(message: types.Message):
    user = db.get_user_data(message.from_user.id)
    
    await message.answer("Settings", reply_markup=settings_menu(user))


@dp.callback_query_handler(image_callback.filter())
async def image_settings_callback(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    value = callback_data.get("value") == "True"
    db.update_user_settings(call.from_user.id, "image", not value)
    user = db.get_user_data(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=settings_menu(user))


@dp.callback_query_handler(subscription_callback.filter(command="subscribe"))
async def subscribe_callback(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    command = callback_data.get("command")
    if (not db.subscriber_exists(call.from_user.id)):
        # if user do not exist add user to db
        db.add_subscriber(call.from_user.id)
    elif db.subscriber_status(call.from_user.id):
        await call.message.answer("You are already subscribed to the notifications!")
    else:
        # if user exist, update status
        db.update_subscription(call.from_user.id, True)
        await call.message.answer("You have successfully subscribed to the notifications!")


@dp.callback_query_handler(subscription_callback.filter(command="unsubscribe"))
async def unsubscribe_callback(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    command = callback_data.get("command")
    if (not db.subscriber_exists(call.from_user.id)):
        # if user do not exist add user to db
        db.add_subscriber(call.from_user.id, False)
    elif not db.subscriber_status(call.from_user.id):
        await call.message.answer("You are not subscribed :(")
    else:
        # if user exist, update status
        db.update_subscription(call.from_user.id, False)
        await call.message.answer("You have successfully unsubscribed from the notifications :(")


@dp.callback_query_handler(get_data_callback.filter())
async def get_data_callback(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    type = callback_data.get("type")
    user = db.get_user_data(call.from_user.id)
    if user:
        # if user's data exist, send information
        login = user["login"]
        password = user["password"]
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text="We are proceeding your request! Please wait!")
        account, error = await data.get(login, password, type)
        if error:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=account["message"])
        else:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'Name: {account.get("username")}\nAccount name: {account.get("name")}\nBalance: {account.get("balance")}')
            if user["image"]:
                await bot.send_photo(chat_id=call.from_user.id, photo=open(f'{account["image"]}', "rb"))
    else:
        # if user's data do not exist, ask to enter login and password
        await call.answer("We don't have your login and password, please use '/register login password' command")


@dp.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # if user do not exist add user to db
        db.add_subscriber(message.from_user.id)
    else:
        # if user exist, update status
        db.update_subscription(message.from_user.id, True)

    await message.answer("You have successfully subscribed to the notifications!")


@dp.message_handler(commands=["unsubscribe"])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # if user do not exist add user to db
        db.add_subscriber(message.from_user.id, False)
        await message.answer("You are not subscribed.")
    else:
        # if user exist, update status
        db.update_subscription(message.from_user.id, False)
        await message.answer("You have successfully unsubscribed from the notifications.")


@dp.message_handler(commands=["register"])
async def register(message: types.Message):
    arguments = message.get_args().split()
    if len(arguments) != 2:
        await message.answer("There is an error in your input.\nPlease try to follow the instructions")
    else:
        login, password = arguments
        db.update_user_data(message.from_user.id, login, password)
        await message.answer("We recorded your data!\nNow you can use all functions of our bot!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
