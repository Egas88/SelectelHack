from telebot import types

from bot import bot


def handle_menu(message):
    # menu_
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Донации
    donation_btn = types.InlineKeyboardButton('Донации', callback_data='menu_donations')

    ######

    # Центры крови

    centers_btn = types.InlineKeyboardButton('Центры крови', callback_data='menu_centers')

    ######

    # Геймификация

    gamification_btn = types.InlineKeyboardButton('Геймификация', callback_data='menu_gamification')

    #####

    # Личное

    personal_btn = types.InlineKeyboardButton('Личное', callback_data='menu_personal')

    # back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')

    ######

    # Статьи
    articles_btn = types.InlineKeyboardButton('Статьи из журнала', callback_data='menu_articles')

    # Бонусы
    bonuses_btn = types.InlineKeyboardButton('Запросить бонусы', callback_data='menu_bonuses')

    ######
    markup.add(donation_btn, centers_btn, gamification_btn, personal_btn, articles_btn, bonuses_btn)

    img = "img/logo.jpg"
    msg_text = """
    <b>🩸 Добро пожаловать в Телеграм Бота DonorSearch! 💉</b>
      
🌟 Здесь вы можете найти информацию о центрах крови, планировать свои донации, узнать о бонусах и статусе геймификации, а также подготовиться к сдаче крови с помощью нашей памятки
👏 Не забудьте также о возможности сделать пожертвование на развитие проекта
🚀 Начните пользоваться DonorSearch прямо сейчас

    """
    bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=msg_text, reply_markup=markup, parse_mode="HTML")

