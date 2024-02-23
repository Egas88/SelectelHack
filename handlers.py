from telebot import types
from auth_register.register import handle_register
from auth_register.auth import handle_login
from start.start import handle_start
from bot import bot
from blood_station.blood_station import handle_blood_stations_list


@bot.message_handler(commands=['login'])
def login(message):
    handle_login(bot, message)


@bot.message_handler(func=lambda message: message.text == 'Регистрация', commands=['register'])
def register(message):
    handle_register(bot, message)


@bot.message_handler(commands=['start'])
def start(message):
    handle_start(bot, message)

@bot.message_handler(commands=['view'])
def view(message):
    handle_blood_stations_list(message)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Регистрация":
        register(message)
    elif message.text == "Логин":
        login(message)
    else:
        pass

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
