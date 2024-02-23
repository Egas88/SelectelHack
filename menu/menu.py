from telebot import types

from bot import bot


def handle_menu(message):
    # menu_
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_donation_button = types.InlineKeyboardButton('Добавить донацию', callback_data='menu_add_donation')
    plan_donation_button = types.InlineKeyboardButton('Запланировать донацию', callback_data='menu_plan_donation')
    blood_stations_button = types.InlineKeyboardButton('Запросить карточки центров крови',
                                                       callback_data='menu_blood_stations')
    address_needs_button = types.InlineKeyboardButton('Запросить адресные потребности',
                                                      callback_data='menu_address_needs')
    bonuses_button = types.InlineKeyboardButton('Запросить бонусы', callback_data='menu_bonuses')
    top_status_button = types.InlineKeyboardButton('Узнать статус геймификации в топе', callback_data='menu_top_status')
    honorary_donor_button = types.InlineKeyboardButton('Запросить статус до почетного донора',
                                                       callback_data='menu_honorary_donor')
    specific_donation_button = types.InlineKeyboardButton('Запросить конкретную донацию',
                                                          callback_data='menu_specific_donation')
    blood_donation_guide_button = types.InlineKeyboardButton('Памятка по подготовке к сдачи крови',
                                                             callback_data='menu_blood_donation_guide')
    games_projects_button = types.InlineKeyboardButton('Игры и спецпроекты', callback_data='menu_games_projects')
    articles_button = types.InlineKeyboardButton('Статьи из журнала', callback_data='menu_articles')
    donate_button = types.InlineKeyboardButton('Сделать пожертвование проекту', callback_data='menu_donate')
    change_personal = types.InlineKeyboardButton('Сменить личные данные', callback_data='menu_change_personal')

    markup.add(add_donation_button, plan_donation_button, blood_stations_button, address_needs_button, bonuses_button,
               top_status_button, honorary_donor_button, specific_donation_button, blood_donation_guide_button,
               games_projects_button, articles_button, donate_button, change_personal)

    bot.send_message(message.chat.id, "Выбирайте!", reply_markup=markup)
