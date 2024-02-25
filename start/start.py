from telebot import types
from bot import bot


def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    reg_button = types.InlineKeyboardButton('Регистрация', callback_data='start_register')
    login_button = types.InlineKeyboardButton('Логин', callback_data='start_login')
    # help_button = types.InlineKeyboardButton('Помощь', callback_data='start_help')
    markup.add(reg_button, login_button)  # , help_button)

    hello_message = """
        <b> Привет! Я бот DonorSearch.</b>
    
💻 Для работы со мной тебе нужно авторизоваться!
    
‼️ Но это не просто авторизация. Это шанс спасти жизнь!
    
🩸 Присоединяйся к сообществу доноров и стань частью проекта, который меняет мир к лучшему!

💓 Сделай свой вклад в благотворительность, стань донором!
    
"""

    bot.send_message(message.chat.id, hello_message, reply_markup=markup, parse_mode="HTML")
