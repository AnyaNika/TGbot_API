# Подгружаем используемые библиотеки
import telebot
from  telebot import types
import random
import requests

from config import TOKEN, NASA_API_KEY

#Вводим заранее полученные ключ NASA и адрес(URL), с которого будем получать фотографии
nasa_api_key = NASA_API_KEY
rover_api_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'


#Создаем класс BotClass в который передаем эти параметры
class BotClass:
    def __init__(self, url: str, key: str):

        self.nasa_api_key = key
        self.rover_api_url = url

#В классе создаем метод get_url_photo который возвращает URL фотографии и дату фотографии
    def get_url_photo(self):

        while True:
            random_sol = random.randint(1, 3000)
            params = {'api_key': nasa_api_key, 'sol': random_sol}
            response = requests.get(rover_api_url, params=params).json()
            if response['photos']:
                break

        ph_url = response['photos']
        ph_u1 = ph_url[1]
#возврат параметров
        return ph_u1['img_src'], ph_u1['earth_date']

# Создаем экземпляр класса clitnt
clitnt = BotClass(rover_api_url, nasa_api_key)
# Запускаем бот
bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=['start'])
def start(message):
    mess1 = 'Привет!'
            #'У меня всего две кнопки\n'\
            #'Введите команду\n    /start  \nИ нажмите на любую из них'
    bot.send_message(message.chat.id, mess1,parse_mode= 'html')
# Создаем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Новое фото')
    but2 = types.KeyboardButton('Что я умею')
    markup.add(but1, but2)
    bot.send_message(message.chat.id, 'Я умею выводить фотографии, сделанные марсоходом в разное время.', reply_markup= markup)


@bot.message_handler()
def get_user_text(message):
    if message.text == 'Новое фото':
        p_u, e_d = clitnt.get_url_photo() # используем метод для получения URL и даты фотографии
        caption = f'Фотография сделана {e_d}'
        bot.send_photo(message.chat.id, p_u, caption = caption) # отправляем фото с подписью в бот


    elif message.text == 'Что я умею':

        bot.send_message(message.chat.id, 'Я умею выводить фотографии, сделанные марсоходом в разное время.')
    else:
        mess = 'Не сбивайте меня непонятными командами.\n'\
            'Я очень простой бот, у меня всего две кнопки.\n'\
            'Введите команду  /start  \nи нажмите на любую из них.'

        bot.send_message(message.chat.id, text=mess)
bot.polling(none_stop=True)