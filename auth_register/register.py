import requests
from telebot import types
from bot import bot
from auth_register.validators import password_validator, email_validator, phone_validator
from api import *

cur_user_data = {}

def handle_register(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите Ваше имя")
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    cur_user_data["name"] = message.text
    markup = types.ReplyKeyboardMarkup(row_width=1)
    email_btn = types.KeyboardButton('По Email')
    phone_btn = types.KeyboardButton('По номеру телефона')
    markup.add(email_btn, phone_btn)
    bot.send_message(message.from_user.id, "Пожалуйста, выберите тип регистрации:", reply_markup=markup)
    bot.register_next_step_handler(message, process_register_step)


def process_register_step(message):
    user_id = message.from_user.id
    if message.text == "По Email":
        bot.send_message(user_id, "Введите ваш email:")
        bot.register_next_step_handler(message, process_email_step)
    elif message.text == "По номеру телефона":
        bot.send_message(user_id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(message, process_phone_step)
    else:
        bot.send_message(user_id, "Пожалуйста, выберите один из вариантов.")


def process_email_step(message):
    user_id = message.from_user.id
    email = message.text
    if not email_validator(email):
        bot.send_message(user_id, "Извините, ваш Email некорректен. Введите верный Email")
        bot.register_next_step_handler(message, process_email_step)
        return
    cur_user_data["email"] = message.text
    bot.send_message(user_id, "Введите пароль для Вашей учетной записи", disable_web_page_preview=True)
    bot.register_next_step_handler(message, process_password_step, "email")


def process_phone_step(message):
    user_id = message.from_user.id
    phone = message.text
    is_valid, formatted_phone = phone_validator(phone)
    if not is_valid:
        bot.send_message(user_id, "Извините, ваш телефон некорректен. Введите верный мобильный номер")
        bot.register_next_step_handler(message, process_phone_step)
        return

    cur_user_data["phone"] = formatted_phone
    bot.send_message(user_id, "Введите пароль для Вашей учетной записи", disable_web_page_preview=True)
    bot.register_next_step_handler(message, process_password_step, "phone")


def process_password_step(message, reg_type):
    user_id = message.from_user.id
    password = message.text
    if not password_validator(password):
        bot.send_message(user_id, "Извините, ваш пароль слишком простой. Не забывайте использовать цифры, строчные и "
                                  "прописные буквы, а также спецсимволы")
        bot.register_next_step_handler(message, process_password_step, reg_type)
        return

    cur_user_data["password"] = message.text

    if reg_type == "phone":
        bot.send_message(user_id, "На указанный номер было выслато сообщение с СМС кодом. Введите его ниже для "
                                  "подтверждения")
        body = {
            "phone": cur_user_data["phone"],
            "password": cur_user_data["password"],
            "first_name": cur_user_data["name"],
            "tag": "string"
        }

    elif reg_type == "email":
        bot.send_message(user_id, "На указанный Email было выслато сообщение с кодом. Введите его ниже для "
                                  "подтверждения.")
        body = {
            "email": cur_user_data["email"],
            "password": cur_user_data["password"],
            "first_name": cur_user_data["name"],
            "tag": "string"
        }

    else:
        return

    resp = requests.post(API_AUTH_REGISTRATION, data=body)
    cur_user_data["user_id"] = resp.json()["user_id"]
    bot.register_next_step_handler(message, process_confirm_reg, reg_type)
    print(resp)


def process_confirm_reg(message, reg_type):
    user_id = message.from_user.id
    code = message.text

    body = {
        "code": code,
        "user_id": cur_user_data["user_id"],
        reg_type: cur_user_data["email"] if "email" in cur_user_data else cur_user_data["phone"]
    }

    if reg_type == "email":
        resp = requests.post(API_AUTH_CONFIRM_EMAIL_REG, data=body)
    elif reg_type == "phone":
        resp = requests.post(API_AUTH_CONFIRM_PHONE_REG, data=body)
    else:
        return

    if resp.status_code == 200:
        cur_user_data["username"] = resp.json()["username"]
        bot.send_message(user_id, "Вы были успешно зарегистрированы!")
    else:
        bot.send_message(user_id, "Введённый Вами код неверен, введите его ещё раз:")
        bot.register_next_step_handler(message, process_confirm_reg, reg_type)
