import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
