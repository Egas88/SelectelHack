import requests
from auth_register.validators import phone_validator, email_validator
from auth_register.users import users_dict
from bot import bot
from api import *
from menu.menu import handle_menu

cur_user_data = {}


def handle_login(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите ваш логин")
    bot.register_next_step_handler(message, process_username_step)


def process_username_step(message):
    user_id = message.chat.id
    username = message.text
    cur_user_data["username"] = username
    bot.send_message(user_id, "Введите ваш пароль")
    bot.register_next_step_handler(message, process_password_step)


def process_password_step(message):
    user_id = message.chat.id
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
            bot.send_message(user_id, "Введите корректный логин")
            bot.register_next_step_handler(message, process_password_step)
            return

    if phone is not None:
        cur_user_data["username"] = phone

    cur_user_data["password"] = password
    body = {
        "username": cur_user_data["username"],
        "password": cur_user_data["password"],
    }

    resp = requests.post(API_AUTH_LOGIN, data=body)
    if resp.status_code == 200:
        bot.send_message(user_id, "Вы были успешно авторизированы!")
        users_dict[message.chat.id] = cur_user_data
        handle_menu(message)

    else:
        bot.send_message(user_id, "Введённые данные неверны")

