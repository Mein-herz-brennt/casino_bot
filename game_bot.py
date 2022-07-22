from main import bot, dp
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint
from casinostate import Dice_state, Joe_state
from game_bot_function import Win_or_lose_money

k = 3000
fruit = {1: '🍎', 2: '🍓', 3: '🍒', 4: '🍋', 5: '🥥'}

head_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
game_button = types.KeyboardButton(text='Перейти к списку игр🎮')
bank_button = types.KeyboardButton(text='Мой баланс💰')
head_keyboard.add(game_button).add(bank_button)

bank_keyboard = types.ReplyKeyboardMarkup()
cash_button = types.KeyboardButton(text='Вивести деньги💸')
deposit_button = types.KeyboardButton(text='Пополнить Баланс💳')
back_button = types.KeyboardButton(text='Назад')
bank_keyboard.add(cash_button).add(deposit_button).add(back_button)

game_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
game_button1 = types.KeyboardButton(text="Кости🎲")
game_button2 = types.KeyboardButton(text="Однорукий Джо🎰")
back_button = types.KeyboardButton(text='Назад')
game_keyboard.add(game_button1, game_button2).add(back_button)

dice_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
throw1 = types.KeyboardButton(text='Бросить один кубик')
throw2 = types.KeyboardButton(text='Бросить два кубика')
change_button = types.KeyboardButton(text='Сменить ставку')
back_button = types.KeyboardButton(text='Назад')
dice_keyboard.add(throw1, throw2).add(change_button).add(back_button)

rate_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
rate_button = types.KeyboardButton(text='Сделать ставку')
back_button = types.KeyboardButton(text='Назад')
rate_keyboard.add(rate_button).add(back_button)

slots_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
wheel_button = types.KeyboardButton(text='Вращать барабан')
change_button = types.KeyboardButton(text='Сменить ставку')
back_button = types.KeyboardButton(text='Назад')
slots_keyboard.add(wheel_button).add(change_button).add(back_button)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    global k
    k += 3000
    await message.answer('Вітаємо у нашому закладі! Якщо ви тут вперше то вам сюди  => \n /help',
                         reply_markup=head_keyboard)
    await message.answer_dice()


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.answer('тут буде знаходитись інформація про команди та допоміжний інструментарій')


@dp.message_handler(text='Перейти к списку игр🎮')
async def game(message: Message):
    await message.answer('вот список доступных игр', reply_markup=game_keyboard)


@dp.message_handler(text='Мой баланс💰')
async def bank(message: Message):
    await message.answer(f'Ваш баланс становит {k} рублей', reply_markup=bank_keyboard)


@dp.message_handler(text='Вивести деньги💸')
async def cash_out(message: Message):
    await message.answer('тут буде реалізовано вивід коштів на карту')


@dp.message_handler(text='Пополнить Баланс💳')
async def deposit(message: Message):
    await message.answer('тут буде реалізовано поповнення ігрового балансу')


@dp.message_handler(text='Назад')
async def back(message: Message):
    await message.answer('Ви вернулись в главное меню', reply_markup=head_keyboard)


@dp.message_handler(text='Кости🎲', state=None)
async def dice(message: Message):
    await message.answer(f'Ваш баланс: {k}\n', reply_markup=rate_keyboard)

    await Dice_state.rax.set()


@dp.message_handler(state=Dice_state.rax)
async def rax_msg(message: Message, state: FSMContext):
    if message.text == 'Сделать ставку':
        await message.answer('Введите свою ставку')
        await Dice_state.rate.set()
    elif message.text == 'Назад':
        await state.finish()
        await message.answer('Ви вернулись в меню игр', reply_markup=game_keyboard)


@dp.message_handler(state=Dice_state.rate)
async def rate(message: Message, state: FSMContext):
    global rat, k
    rat = int(message.text)
    if rat <= k:
        await message.answer('Чтоби начать нажмите кнопку бросить кости', reply_markup=dice_keyboard)
        await Dice_state.first.set()
    else:
        await state.finish()
        await message.reply('Ваша ставка не должна превышать ваш баланс!')


@dp.message_handler(state=Dice_state.first)
async def throw_dice(message: Message, state: FSMContext):
    global k
    get_text_msg = message.text
    if get_text_msg == 'Бросить один кубик':
        his_num = randint(1, 6)
        bot_num = randint(1, 6)
        if his_num > bot_num:
            k -= rat
            win = Win_or_lose_money(rat).give_cash()
            k += win
            await message.answer(f"Ваше число: {his_num} \n Число бота: {bot_num} \n Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {win} \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
        elif his_num < bot_num:
            lose = rat
            k -= lose
            await message.answer(f"Ваше число: {his_num} \n Число бота: {bot_num} \n Вас настигла неудача! \n "
                                 f"Ваш проигрыш составил: {lose} \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
        elif his_num == bot_num:
            await message.answer(f"Ваше число: {his_num} \n Число бота: {bot_num} \n Неужели ничья! \n "
                                 "Все остались при своём \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
    elif get_text_msg == 'Бросить два кубика':
        his_num1 = randint(1, 6)
        his_num2 = randint(1, 6)
        bot_num1 = randint(1, 6)
        bot_num2 = randint(1, 6)
        his_num_sum = his_num1 + his_num2
        bot_num_sum = bot_num1 + bot_num2
        if his_num_sum > bot_num_sum:
            k -= rat
            win = Win_or_lose_money(rat).give_cash()
            k += win
            await message.answer(f"Сума чисел на ваших кубиках: {his_num_sum} \n "
                                 f"Сума чисел на кубиках бота : {bot_num_sum} \n"
                                 "Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {win} \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
        elif his_num_sum < bot_num_sum:
            lose = rat
            k -= lose
            await message.answer(f"Сума чисел на ваших кубиках: {his_num_sum} \n "
                                 f"Сума чисел на кубиках бота : {bot_num_sum} \n"
                                 "Вас настигла неудача! \n "
                                 f"Ваш проигрыш составил: {lose} \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
        elif his_num_sum == bot_num_sum:
            await message.answer(f"Сума чисел на ваших кубиках: {his_num_sum} \n "
                                 f"Сума чисел на кубиках бота : {bot_num_sum} \n"
                                 f"Неужели ничья! \n "
                                 f"Все остались при своём \n"
                                 f"Ваш баланс: {k}", reply_markup=dice_keyboard)
            await Dice_state.first.set()
    elif get_text_msg == 'Назад':
        await state.finish()
        await message.answer('Ви вернулись в меню игр', reply_markup=game_keyboard)
    elif get_text_msg == 'Сменить ставку':
        await Dice_state.rax.set()
        await message.answer('Смените ставку', reply_markup=rate_keyboard)
    else:
        await state.finish()
        await message.reply('Извини но я не знаю что это значит! \n Попробуй нажать кнопку "Назад" ')
    if k <= 0:
        await state.finish()
        await message.answer('ОЙ, у вас закончились деньги на игровом щету', reply_markup=head_keyboard)
    elif k < rat:
        await state.finish()
        await message.answer('Денег на вашем балансе не хватает чтобы совершить следующую ставку\n'
                             f'Ваш баланс: {k}\n'
                             f'Ваша ставка: {rat}\n'
                             'Чтобы продолжить игру уменьшите ставку, или пополните баланс!',
                             reply_markup=game_keyboard)


@dp.message_handler(text='Однорукий Джо🎰')
async def slots(message: Message):
    await message.answer(f'Ваш баланс: {k}\n', reply_markup=rate_keyboard)
    await Joe_state.rax.set()


@dp.message_handler(state=Joe_state.rax)
async def rax_slots(message: Message, state: FSMContext):
    if message.text == 'Сделать ставку':
        await message.answer('Введите свою ставку')
        await Joe_state.rate.set()
    elif message.text == 'Назад':
        await state.finish()
        await message.answer('Ви вернулись в меню игр', reply_markup=game_keyboard)


@dp.message_handler(state=Joe_state.rate)
async def slot_rate(message: Message, state: FSMContext):
    global slots_rate
    slots_rate = int(message.text)
    if slots_rate <= k:
        await message.answer('Чтобы начать нажмите кнопку чтоби вращать барабан', reply_markup=slots_keyboard)
        await Joe_state.first.set()
    else:
        await state.finish()
        await message.reply('Ваша ставка не должна превышать ваш баланс!')


@dp.message_handler(state=Joe_state.first)
async def joe(message: Message, state: FSMContext):
    slot_sms = message.text
    global k
    if slot_sms == 'Вращать барабан':
        slots_win = 0
        r1 = randint(1, 5)
        r2 = randint(1, 5)
        r3 = randint(1, 5)
        if r1 == r2 == r3:
            k -= slots_rate
            slots_win += randint(slots_rate + 100, slots_rate + 500)
            k += slots_win
            await message.answer(f"ПОБЕДНЫЙ---{fruit[r1]}{fruit[r2]}{fruit[r3]}---ПОБЕДНЫЙ\n"
                                 "Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {slots_win} \n"
                                 f"Ваш баланс: {k}")
        elif r1 == r2:
            k -= slots_rate
            slots_win += randint(slots_rate + 5, slots_rate + 50)
            k += slots_win
            await message.answer(f"ПОБЕДНЫЙ---{fruit[r1]}{fruit[r2]}{fruit[r3]}---ПОБЕДНЫЙ\n"
                                 "Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {slots_win} \n"
                                 f"Ваш баланс: {k}")
        elif r2 == r3:
            k -= slots_rate
            slots_win += randint(slots_rate + 5, slots_rate + 50)
            k += slots_win
            await message.answer(f"ПОБЕДНЫЙ---{fruit[r1]}{fruit[r2]}{fruit[r3]}---ПОБЕДНЫЙ\n"
                                 "Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {slots_win} \n"
                                 f"Ваш баланс: {k}")
        elif r1 == r3:
            k -= slots_rate
            slots_win += randint(slots_rate + 5, slots_rate + 50)
            k += slots_win
            await message.answer(f"ПОБЕДНЫЙ---{fruit[r1]}{fruit[r2]}{fruit[r3]}---ПОБЕДНЫЙ\n"
                                 "Ваша взяла! \n "
                                 f"Ваш выигрыш составил: {slots_win} \n"
                                 f"Ваш баланс: {k}")
        else:
            k -= slots_rate
            await message.answer(f"проиграшный---{fruit[r1]}{fruit[r2]}{fruit[r3]}---проиграшный\n"
                                 "Вас настигла неудача! \n "
                                 f"Ваш проигрыш составил: {slots_rate} \n"
                                 f"Ваш баланс: {k}")
    elif slot_sms == 'Назад':
        await state.finish()
        await message.answer('Ви вернулись в меню игр', reply_markup=game_keyboard)
    elif slot_sms == 'Сменить ставку':
        await Joe_state.rax.set()
        await message.answer('Смените ставку', reply_markup=rate_keyboard)
    else:
        await state.finish()
        await message.reply('Извини но я не знаю что это значит! \n Попробуй нажать кнопку "Назад" ')
    if k <= 0:
        await state.finish()
        await message.answer('ОЙ, у вас закончились деньги на игровом щету', reply_markup=head_keyboard)
    elif k < slots_rate:
        await state.finish()
        await message.answer('Денег на вашем балансе не хватает чтобы совершить следующую ставку\n'
                             f'Ваш баланс: {k}\n'
                             f'Ваша ставка: {slots_rate}\n'
                             'Чтобы продолжить игру уменьшите ставку, или пополните баланс!',
                             reply_markup=game_keyboard)
