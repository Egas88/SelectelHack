from telebot import types

from auth_register.change_creds.change_creds import handle_change_creds
from auth_register.register import handle_register
from auth_register.auth import handle_login
from menu.menu import handle_menu
from menu.menu_handlers import *
from start.start import handle_start
from donation.donation import handle_donation_adding
from auth_register.users import users_dict
from bot import bot
from blood_station.blood_station import handle_blood_stations_list, handle_blood_stations_need_list


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    # Создаем кнопку "Start"
    start_button = types.KeyboardButton('/start')

    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(start_button)

    handle_start(message)


@bot.message_handler(commands=['view'])
def view(message):
    handle_blood_stations_list(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('start_'))
def message_reply(callback):
    if callback.data == "start_register":
        if callback.message.chat.id in users_dict:
            bot.send_message(callback.message.chat.id, "Вы уже авторизованы!")
            handle_menu(callback.message)
        else:
            handle_register(callback.message)
    elif callback.data == "start_login":
        if callback.message.chat.id in users_dict:
            bot.send_message(callback.message.chat.id, "Вы уже авторизованы!")
            handle_menu(callback.message)
        else:
            handle_login(callback.message)
    else:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
def message_reply(callback):
    if callback.data == "menu_donations":
        handle_donations_menu(callback.message)
    elif callback.data == "menu_centers":
        handle_blood_centers_menu(callback.message)
    elif callback.data == "menu_gamification":
        handle_gamification_menu(callback.message)
    elif callback.data == "menu_personal":
        handle_personal_menu(callback.message)
    elif callback.data == "menu_articles":
        handle_articles_menu(callback.message)
    elif callback.data == "menu_bonuses":
        pass
    else:
        return


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
