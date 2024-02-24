import telebot
import os
from dotenv import load_dotenv

load_dotenv()

#print(os.getenv('BOT_TOKEN'))
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
