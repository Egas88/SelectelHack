from telebot import types


def handle_register(bot, message):
    bot.send_message(message.from_user.id, "Пожалуйста, выберите тип регистрации:")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    email_btn = types.KeyboardButton('Email')
    phone_btn = types.KeyboardButton('По номеру телефона')
    markup.add(email_btn, phone_btn)

def email_register(bot, message):
    ...


def phone_register(bot, message):
    ...
