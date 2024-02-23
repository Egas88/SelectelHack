from telebot import types
from bot import bot


def handle_blood_donation_guide(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    guide_link = types.InlineKeyboardButton('📕 Полный справочник ',
                                            url="https://journal.donorsearch.org/category/directory/")
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> 📕 Справочник донора  </b>

💉 Можно стать донором в 18-55 лет (до 60 - плазма). Минимальный вес - 50 кг.

📝 Перед сдачей необходимо пройти медосмотр. Запрещено употреблять лекарства, алкоголь, наркотики.

🥪 Нельзя есть жирную и острую пищу за 3 часа до сдачи. Бананы, орехи, молоко - за сутки.

⌚ Интервал между сдачами: мужчины - не чаще чем через 2 месяца, женщины - через 3.

🏆 За сдачу полагаются компенсации (деньги, награды, почет).

🆘 Заразиться при сдаче нельзя, используются одноразовые наборы. Центры крови - самые стерильные места!

💪 Будьте донорами! Ваша кровь - это жизнь для пациентов!

Более подробнее Вы можете изучить донорство по кнопке ниже

    """
    markup.add(guide_link, back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
