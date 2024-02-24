import requests
from telebot import types

from api import *
from auth_register import users
from auth_register.validators import password_validator, phone_validator, email_validator
from bot import bot
from auth_register.users import users_dict, get_password, get_username
from menu.menu import handle_menu


def handle_change_creds(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    change_email_button = types.InlineKeyboardButton('📧 Сменить Email', callback_data='change_email')
    change_phone_button = types.InlineKeyboardButton('☎️ Сменить Телефон', callback_data='change_phone')
    change_password_button = types.InlineKeyboardButton('🔑 Сменить пароль', callback_data='change_password')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    markup.add(change_email_button, change_phone_button, change_password_button, back_button)

    hello_message = """
        <b> Смена личных данных</b>

💻 Вы можете сменить свой Email, телефон или пароль!


    """

    bot.send_message(message.chat.id, hello_message, reply_markup=markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_'))
def process_register_step(callback):
    chat_id = callback.message.chat.id
    if callback.data == "change_email":
        if not users.is_possible_input:
            return
        else:
            users.is_possible_input = False
        bot.send_message(chat_id, "📧 Введите новый email:")
        bot.register_next_step_handler(callback.message, process_email_change)
    elif callback.data == "change_phone":
        if not users.is_possible_input:
            return
        else:
            users.is_possible_input = False
        bot.send_message(chat_id, "☎️ Введите новый телефона:")
        bot.register_next_step_handler(callback.message, process_phone_change)
    elif callback.data == "change_password":
        if not users.is_possible_input:
            return
        else:
            users.is_possible_input = False
        bot.send_message(chat_id, "🔑 Введите новый пароль!")
        bot.register_next_step_handler(callback.message, process_password_change)
    elif callback.data == "change_go_back":
        handle_menu(callback.message)
    else:
        return


def process_password_change(message):
    chat_id = message.chat.id
    password1 = message.text

    if not password_validator(password1):
        bot.send_message(chat_id, "Извините, ваш пароль слишком простой.\n Не забывайте использовать цифры, строчные и "
                                  "прописные буквы, а также спецсимволы")
        bot.register_next_step_handler(message, process_password_change)
        return

    bot.send_message(chat_id, "🔑 Повторите новый пароль!")

    def retype_new_password(message):
        password2 = message.text

        if password1 != password2:
            bot.send_message(chat_id, "Пароли должны совпадать!")
            bot.register_next_step_handler(message, process_password_change)
            return

        body = {
            "password1": password1,
            "password2": password2,
        }

        resp = requests.post(API_AUTH_CHANGE_PASSWORD, data=body,
                             auth=(get_username(chat_id), get_password(chat_id)))
        if resp.status_code == 200:
            users_dict[chat_id]["password"] = password1
            bot.send_message(chat_id, "Пароль успешно изменён!")
            users.is_possible_input = True

            handle_menu(message)
        else:
            return

    bot.register_next_step_handler(message, retype_new_password)


def process_phone_change(message):
    chat_id = message.chat.id
    phone = message.text
    is_valid, formatted_phone = phone_validator(phone)
    if not is_valid:
        bot.send_message(chat_id, "Извините, введённый номер некорректен.\nВведите верный мобильный номер")
        bot.register_next_step_handler(message, process_phone_change)
        return

    body = {
        "phone": formatted_phone,
    }

    resp = requests.post(API_AUTH_CHANGE_PHONE, data=body,
                         auth=(get_username(chat_id), get_password(chat_id)))
    if resp.status_code == 200:
        users_dict[chat_id]["phone"] = formatted_phone
        bot.send_message(chat_id, "Телефон успешно изменён!")
        users.is_possible_input = True

        handle_menu(message)
    else:
        return


def process_email_change(message):
    chat_id = message.chat.id

    email = message.text
    if not email_validator(email):
        bot.send_message(chat_id, "Извините, введённый Email некорректен. Введите верный Email")
        bot.register_next_step_handler(message, process_email_change)
        return

    body = {
        "email": email,
    }
    resp = requests.post(API_AUTH_CHANGE_EMAIL, data=body,
                         auth=(get_username(chat_id), get_password(chat_id)))

    if resp.status_code == 200:
        users_dict[chat_id]["email"] = email
        bot.send_message(chat_id, "Email успешно изменён!")
        users.is_possible_input = True

        handle_menu(message)
    else:
        return
