from telebot import types

import auth_register.users as users
from auth_register.change_creds.change_creds import handle_change_creds
from auth_register.register import handle_register
from auth_register.auth import handle_login
from menu.menu import handle_menu
from bonuses.bonuses import handle_view_bonuses_list
from menu.menu_handlers import *
from start.start import handle_start
from donation.donation import handle_donation_adding
from auth_register.users import users_dict
from bot import bot
from blood_station.blood_station import handle_blood_stations_list
from db.create_data import create_notifications_table


@bot.message_handler(commands=['start'])
def start(message):
    handle_start(message)


@bot.message_handler(commands=['viewBonuses'])
def view_bonuses_list(message):
    handle_view_bonuses_list(message)


@bot.message_handler(commands=['view'])
def view(message):
    handle_blood_stations_list(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_'))
def back_button(callback):
    if callback.data == "back_start":
        users.is_reg = False
        users.is_login = False
        users.is_change_pass = False
        users.is_change_phone = False
        users.is_change_email = False
        users.is_possible_input = True
        handle_start(callback.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('start_'))
def message_reply(callback):
    if callback.data == "start_register":
        if users.is_reg or users.is_login or users.is_change_pass or users.is_change_phone or users.is_change_email:
            return
        users.is_reg = True
        if not users.is_possible_input:
            return
        else:
            users.is_possible_input = False
        if callback.message.chat.id in users_dict:
            bot.send_message(callback.message.chat.id, "Вы уже авторизованы!")
            users.is_possible_input = True
            handle_menu(callback.message)
        else:
            handle_register(callback.message)
    elif callback.data == "start_login":
        if users.is_reg or users.is_login or users.is_change_pass or users.is_change_phone or users.is_change_email:
            return
        users.is_login = True
        if not users.is_possible_input:
            return
        else:
            users.is_possible_input = False

        if callback.message.chat.id in users_dict:
            bot.send_message(callback.message.chat.id, "Вы уже авторизованы!")
            users.is_possible_input = True
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
        handle_view_bonuses_list(callback.message)
    else:
        return


if __name__ == "__main__":
    create_notifications_table()
    bot.polling(none_stop=True, interval=0)
