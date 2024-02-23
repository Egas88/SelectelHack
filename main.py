import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, пошёл нахуй!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Пошёл нахуй!.")



bot.polling(none_stop=True, interval=0)