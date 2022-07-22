import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from discret_state import Admin_password

numbers = {}

storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token='1877552643:AAFEHYiePy513LpsdVI1XSq5Hpsge5eDO-M', parse_mode='html')
dp = Dispatcher(bot, loop=loop, storage=storage)


@dp.message_handler(text="Білет №:")
async def get_start_bilet(msg: types.Message, state: FSMContext):
    await msg.answer('Введіть номер білету')
    await Admin_password.a.set()


@dp.message_handler(state=Admin_password.a)
async def check_bilet(msg: types.Message):
    global numbers
    numbers[msg.text] = ["@" + msg.chat.username]
    if msg.text in numbers.keys():
        for i in numbers[msg.text]:
            await msg.answer(i)


executor.start_polling(dp, skip_updates=True)
