from telebot import types
from bot import bot


def handle_change_creds(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    change_email_button = types.InlineKeyboardButton('📧 Сменить Email', callback_data='change_email')
    change_phone_button = types.InlineKeyboardButton('☎️ Сменить Телефон', callback_data='change_phone')
    change_password_button = types.InlineKeyboardButton('🔑 Сменить пароль', callback_data='change_password')
    back_button = types.InlineKeyboardButton('↩️ Назад ')
    markup.add(change_email_button, change_phone_button, change_password_button)

    hello_message = """
        <b> Смена личных данных</b>

    💻 Вы можете сменить свой Email, телефон или пароль!

    """

    bot.send_message(message.chat.id, hello_message, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_'))
def process_register_step(callback):
    user_id = callback.message.chat.id
    if callback.data == "change_email":
        bot.send_message(user_id, "Введите ваш email:")
        bot.register_next_step_handler(callback.message, process_email_change)
    elif callback.data == "change_phone":
        bot.send_message(user_id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(callback.message, process_phone_change)
    elif callback.data == "change_password":
        bot.send_message(user_id, "Введите ваш текущий пароль:")
        bot.register_next_step_handler(callback.message, process_password_change)

    else:
        return

def process_password_change(message):
    user_id = message.chat.id
    email = message.text

def process_phone_change(message):
    user_id = message.chat.id
    email = message.text

def process_email_change(message):
    user_id = message.chat.id
    email = message.text

