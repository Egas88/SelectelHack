import requests
from telebot import types

from auth_register import users
from auth_register.validators import phone_validator, email_validator
from auth_register.users import users_dict
from bot import bot
from api import *
from menu.menu import handle_menu

cur_user_data = {}


def handle_login(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('↩️ В начало ', callback_data='back_start')

    msg_txt = """
    
    ✏️  Введите ваш логин!

    """
    markup.add(back_button)

    bot.send_message(chat_id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(message, process_username_step)


def process_username_step(message):
    chat_id = message.chat.id
    username = message.text
    cur_user_data["username"] = username

    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('↩️ В начало ', callback_data='back_start')
    markup.add(back_button)

    msg_txt = """

    🔒  Введите ваш пароль!

    """
    if users.additional_input:
        users.additional_input = False
        bot.send_message(chat_id, msg_txt, reply_markup=markup, parse_mode="HTML")
    else:
        return

    bot.register_next_step_handler(message, process_password_step)


def process_password_step(message):
    chat_id = message.chat.id
    password = message.text
    is_valid = False

    phone = None
    try:
        is_valid = email_validator(cur_user_data["username"])
    except Exception as e:
        return
    if not is_valid:
        try:
            is_valid, phone = phone_validator(cur_user_data["username"])
        except Exception as e:
            return
        if not is_valid:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('↩️ В начало ', callback_data='back_start')
            markup.add(back_button)

            msg_txt = """

            ❗  Введите корректный логин!

            """

            bot.send_message(chat_id, msg_txt, reply_markup=markup, parse_mode="HTML")

            bot.register_next_step_handler(message, process_password_step)
            return

    if phone is not None:
        cur_user_data["username"] = phone
        cur_user_data["phone"] = phone
    else:
        cur_user_data["email"] = cur_user_data["username"]

    cur_user_data["password"] = password
    body = {
        "username": cur_user_data["username"],
        "password": cur_user_data["password"],
    }

    resp = requests.post(API_AUTH_LOGIN, data=body)
    if resp.status_code == 200:
        new_message = bot.send_message(chat_id, "✔️ Вы были успешно авторизированы!")
        for i in range(0, 3):
            bot.delete_message(chat_id=message.chat.id, message_id=new_message.message_id - (2 + i))
        users_dict[message.chat.id] = cur_user_data
        users.additional_input = True
        users.is_possible_input = True

        handle_menu(message)

    else:
        users.additional_input = True
        bot.send_message(chat_id, "❌ Введённые данные неверны")
        handle_login(message)
