import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, NASA_API_KEY

# Ваши ключи и URL
nasa_api_key = NASA_API_KEY
rover_api_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
bot_token = TOKEN

# Класс для получения фото
class BotClass:
    def __init__(self, url: str, key: str):
        self.nasa_api_key = key
        self.rover_api_url = url

    def get_url_photo(self):
        while True:
            random_sol = random.randint(1, 3000)
            params = {'api_key': self.nasa_api_key, 'sol': random_sol}
            response = requests.get(self.rover_api_url, params=params).json()
            if response['photos']:
                break
        ph_url = response['photos']
        ph_u1 = ph_url[1] if len(ph_url) > 1 else ph_url[0]
        return ph_u1['img_src'], ph_u1['earth_date']

clitnt = BotClass(rover_api_url, nasa_api_key)

# Создание бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Новое фото"), KeyboardButton(text="Что я умею")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    mess1 = 'Привет!'
    await message.answer(mess1)
    await message.answer(
        "Я умею выводить фотографии, сделанные марсоходом в разное время.",
        reply_markup=keyboard
    )

@dp.message(F.text == "Новое фото")
async def send_new_photo(message: types.Message):
    # Получение фото в отдельном потоке, чтобы не блокировать event loop
    loop = asyncio.get_running_loop()
    p_u, e_d = await loop.run_in_executor(None, clitnt.get_url_photo)
    caption = f'Фотография сделана {e_d}'
    await message.answer_photo(photo=p_u, caption=caption)

@dp.message(F.text == "Что я умею")
async def what_i_can(message: types.Message):
    await message.answer('Я умею выводить фотографии, сделанные марсоходом в разное время.')

@dp.message()
async def unknown(message: types.Message):
    mess = (
        'Не сбивайте меня непонятными командами.\n'
        'Я очень простой бот, у меня всего две кнопки.\n'
        'Введите команду  /start  \nи нажмите на любую из них.'
    )
    await message.answer(mess)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())