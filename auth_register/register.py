import requests
from telebot import types

from auth_register import users
from auth_register.users import users_dict
from bot import bot
from auth_register.validators import password_validator, email_validator, phone_validator
from api import *
from menu.menu import handle_menu

cur_user_data = {}


def handle_register(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('↩️ В начало ', callback_data='back_start')
    markup.add(back_button)

    msg_txt = """

    ✏️  Введите Ваше имя!

    """

    bot.send_message(chat_id, msg_txt, reply_markup=markup, parse_mode="HTML")

    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    cur_user_data["name"] = message.text
    markup = types.InlineKeyboardMarkup(row_width=1)
    email_btn = types.InlineKeyboardButton('📧 По Email', callback_data="register_email")
    phone_btn = types.InlineKeyboardButton('☎️ По номеру телефона', callback_data="register_phone")
    back_button = types.InlineKeyboardButton('↩️ В начало ', callback_data='back_start')

    markup.add(email_btn, phone_btn, back_button)

    if users.additional_input:
        users.additional_input = True
        bot.send_message(message.chat.id, """<b> Пожалуйста, выберите тип регистрации </b> """, reply_markup=markup, parse_mode="HTML")
    else:
        return

@bot.callback_query_handler(func=lambda call: call.data.startswith('register_'))
def process_register_step(callback):
    chat_id = callback.message.chat.id
    if callback.data == "register_email":
        if not users.additional_input:
            return
        else:
            users.additional_input = False
        bot.send_message(chat_id, "✏️  Введите ваш email")
        bot.register_next_step_handler(callback.message, process_email_step)
    elif callback.data == "register_phone":
        if not users.additional_input:
            return
        else:
            users.additional_input = False
        bot.send_message(chat_id, "✏️  Введите ваш номер телефона")
        bot.register_next_step_handler(callback.message, process_phone_step)
    else:
        return


def process_email_step(message):
    chat_id = message.chat.id
    users.additional_input = True

    email = message.text
    if not email_validator(email):
        bot.send_message(chat_id, "❗ Извините, ваш Email некорректен. Введите верный Email")
        bot.register_next_step_handler(message, process_email_step)
        return
    cur_user_data["email"] = message.text

    if users.additional_input:
        users.additional_input = False
        bot.send_message(chat_id, "✏️ Введите пароль для Вашей учетной записи", disable_web_page_preview=True)
    else:
        return

    bot.register_next_step_handler(message, process_password_step, "email")


def process_phone_step(message):
    chat_id = message.chat.id
    users.additional_input = True

    phone = message.text
    is_valid, formatted_phone = phone_validator(phone)
    if not is_valid:
        bot.send_message(chat_id, "❗ Извините, ваш телефон некорректен. Введите верный мобильный номер")
        bot.register_next_step_handler(message, process_phone_step)
        return

    cur_user_data["phone"] = formatted_phone
    if users.additional_input:
        users.additional_input = False
        bot.send_message(chat_id, "✏️ Введите пароль для Вашей учетной записи", disable_web_page_preview=True)
    else:
        return
    bot.register_next_step_handler(message, process_password_step, "phone")


def process_password_step(message, reg_type):
    chat_id = message.chat.id
    password = message.text
    if not password_validator(password):
        msg_txt = """
                <b> ❗ Пароль не соответствует требованиям </b>
                
📏 Длина пароля должна быть больше 8 символов

🔤 Также не забывайте использовать цифры, строчные и заглавные буквы, а также спецсимволы

                """
        bot.send_message(message.chat.id, msg_txt, parse_mode="HTML")

        bot.register_next_step_handler(message, process_password_step, reg_type)
        return

    cur_user_data["password"] = message.text

    if reg_type == "phone":
        bot.send_message(chat_id, "✔️ На указанный номер было выслато сообщение с СМС кодом. Введите его ниже для "
                                  "подтверждения")
        body = {
            "phone": cur_user_data["phone"],
            "password": cur_user_data["password"],
            "first_name": cur_user_data["name"],
            "tag": "string"
        }

    elif reg_type == "email":
        bot.send_message(chat_id, "✔️ На указанный Email было выслато сообщение с кодом. Введите его ниже для "
                                  "подтверждения")
        body = {
            "email": cur_user_data["email"],
            "password": cur_user_data["password"],
            "first_name": cur_user_data["name"],
            "tag": "string"
        }

    else:
        return

    resp = requests.post(API_AUTH_REGISTRATION, data=body)
    if resp.status_code == 200:
        cur_user_data["user_id"] = resp.json()["user_id"]
        bot.register_next_step_handler(message, process_confirm_reg, reg_type)
    else:
        return


def process_confirm_reg(message, reg_type):
    chat_id = message.chat.id
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
        cur_user_data["username"] = cur_user_data["email"] if "email" in cur_user_data else cur_user_data["phone"]
        bot.send_message(chat_id, "✔️ Вы были успешно зарегистрированы!")
        users_dict[message.chat.id] = cur_user_data
        users.additional_input = True
        users.is_reg = False
        users.is_possible_input = True
        handle_menu(message)

    else:
        bot.send_message(chat_id, "❌ Введённый Вами код неверен, повторите ввод ещё раз!")
        bot.register_next_step_handler(message, process_confirm_reg, reg_type)
