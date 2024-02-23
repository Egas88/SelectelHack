from telebot import types


def handle_start(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton('Регистрация', callback_data='register')
    itembtn2 = types.InlineKeyboardButton('Логин', callback_data='login')
    itembtn3 = types.InlineKeyboardButton('Помощь', callback_data='login')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Привет! Я бот DonorSearch. Для регистрации, пожалуйста, выберите способ "
                                      "отправки данных", reply_markup=markup)

