import telebot
import os
from dotenv import load_dotenv
from telebot import types
from auth_register.register import handle_register
from auth_register.auth import handle_login
from start.start import handle_start

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


@bot.message_handler(commands=['login'])
def login(message):
    handle_login(bot, message)


@bot.message_handler(commands=['register'])
def register(message):
    handle_register(bot, message)


@bot.message_handler(commands=['start'])
def start(message):
    handle_start(bot, message)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
