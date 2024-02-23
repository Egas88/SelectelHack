from telebot import types

from auth_register.change_creds.change_creds import handle_change_creds
from auth_register.register import handle_register
from auth_register.auth import handle_login
from menu.menu import handle_menu
from start.start import handle_start
from auth_register.users import users_dict
from bot import bot

@bot.message_handler(commands=['start'])
def start(message):
    handle_start(message)


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
    if callback.data == "menu_change_personal":
        handle_change_creds(callback.message)
    elif callback.data == "start_login":
        pass
    else:
        return




if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
