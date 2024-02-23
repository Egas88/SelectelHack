from telebot import types
from bot import bot


def handle_blood_donation_guide(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Личные настройки ⚙️ </b>

💵 Поддержите наш проект и сделайте мир лучше

✍️ Измените личные данные

🏆 Станьте почетным донором! 

    """
    markup.add(back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")