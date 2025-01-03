import os
import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
# from aiogram.utils import executor
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
load_dotenv()
bot_api_key = os.getenv('INVENTORY_STEWARD_BOT_TOKEN')

dp = Dispatcher()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=bot_api_key, 
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id  # This is their permanent Telegram ID
    username = message.from_user.username  # Their @username if they have one
    print(f"Message from user_id: {user_id}")
    print(f"Message from username: {username}")
    await message.reply("Welcome to the Inventory Management Bot! Type /add to add items.")

@dp.message(Command('add'))
async def add_item(message: types.Message):
    await message.reply("What item would you like to add? Reply with the item name.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())