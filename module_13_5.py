from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Рассчитать'))
kb.insert(KeyboardButton('Информация'))


class UserState(StatesGroup):
    # описываем необходимые нам состояния пользователя
    age = State()
    growth = State()
    weight = State()


# ловим ключевое слово 'calories'
@dp.message_handler(text='Рассчитать')
async def set_age(message):
    # Запрашиваем у пользователя возраст
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# ловим State.age
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    # Получаем введенный возраст от пользователя
    age = message.text

    # Сохраняем введенный возраст в состоянии
    await state.update_data(age=age)

    # Запрашиваем у пользователя рост
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# ловим State.growth
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    # Получаем введенный рост от пользователя
    growth = message.text

    # Сохраняем введенный рост в состоянии
    await state.update_data(growth=growth)

    # Запрашиваем у пользователя вес
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# ловим State.weight
@dp.message_handler(state=UserState.weight)
async def result_info(message, state):
    # Получаем введенный вес от пользователя
    weight = message.text

    # Получаем данные из состояния
    data = await state.get_data()
    age = data.get('age')
    growth = data.get('growth')

    # Выводим информацию
    result = 10 * int(weight) + 6.25 * int(growth) - 5 * int(age) + 5
    await message.answer(f'Ваша дневная норма калорий: {result}')

    # Сбрасываем состояние
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. '
                         'Если хочешь узнать свою суточную норму калорий, нажми кнопку "Рассчитать"', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info_message(message):
    await message.answer('Информация о боте')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
