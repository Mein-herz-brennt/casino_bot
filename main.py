import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from config import TOKEN

storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token='1744432126:AAHDblqtDYp-J1LfTY3R6m-Lz1KfNV4KzgA', parse_mode='html')
dp = Dispatcher(bot, loop=loop, storage=storage)

if __name__ == "__main__":
    from game_bot import *

    executor.start_polling(dp, skip_updates=True)
