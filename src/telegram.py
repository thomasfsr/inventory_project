import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
bot_api_key = os.getenv('INVENTORY_STEWARD_BOT_TOKEN')

bot = Bot(token=bot_api_key, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
