from telebot import types

from auth_register.change_creds.change_creds import handle_change_creds
from bot import bot
from donation.guide import handle_blood_donation_guide


def handle_donations_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    add_donation_button = types.InlineKeyboardButton('Добавить донацию', callback_data='sub_menu_add_donation')
    plan_donation_button = types.InlineKeyboardButton('Запланировать донацию', callback_data='sub_menu_plan_donation')
    specific_donation_button = types.InlineKeyboardButton('Запросить конкретную донацию',
                                                          callback_data='sub_menu_specific_donation')
    blood_donation_guide_button = types.InlineKeyboardButton('Памятка по подготовке к сдачи крови',
                                                             callback_data='sub_menu_blood_donation_guide')

    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Донации 💉 </b>
    
🩸 Здесь вы можете добавить, заплонировать и запросить донацию. 

📃 Также можете получить памятку по подготовке к сдаче крови! 

    """
    markup.add(add_donation_button, plan_donation_button, specific_donation_button, blood_donation_guide_button,
               back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")


def handle_blood_centers_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    blood_stations_button = types.InlineKeyboardButton('Запросить карточки центров крови',
                                                       callback_data='sub_menu_blood_stations')
    address_needs_button = types.InlineKeyboardButton('Запросить адресные потребности',
                                                      callback_data='sub_menu_address_needs')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Центры крови 🩸 </b>
    
🗺️ Здесь вы можете узнать расположение центров крови. 

📍  Также можете найти близжайшитй к Вам центр! 

    """
    markup.add(blood_stations_button, address_needs_button, back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")


def handle_gamification_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    top_status_button = types.InlineKeyboardButton('Узнать статус геймификации в топе',
                                                   callback_data='sub_menu_game_status')
    games_projects_button = types.InlineKeyboardButton('Игры и спецпроекты', callback_data='sub_menu_games_projects')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Геймификация 🕹️ </b>
    
🎲 Узнайте свой стаутс геймификации!

📰 Получите информацию о новейших спецпроектах и играх! 

    """
    markup.add(top_status_button, games_projects_button, back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")


def handle_personal_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    donate_button = types.InlineKeyboardButton('Сделать пожертвование проекту', callback_data='sub_menu_donate')
    change_personal = types.InlineKeyboardButton('Сменить личные данные', callback_data='sub_menu_change_personal')
    honorary_donor_button = types.InlineKeyboardButton('Запросить статус до почетного донора',
                                                       callback_data='sub_menu_honorary_donor')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Личные настройки ⚙️ </b>
    
💵 Поддержите наш проект и сделайте мир лучше

✍️ Измените личные данные

🏆 Станьте почетным донором! 

    """
    markup.add(donate_button, change_personal, honorary_donor_button, back_button)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_menu_'))
def process_register_step(callback):
    if callback.data == "sub_menu_add_donation":
        pass
    elif callback.data == "sub_menu_plan_donation":
        pass
    elif callback.data == "sub_menu_specific_donation":
        pass
    elif callback.data == "sub_menu_blood_donation_guide":
        handle_blood_donation_guide(callback.message)
        pass
    elif callback.data == "sub_menu_blood_stations":
        pass
    elif callback.data == "sub_menu_address_needs":
        pass
    elif callback.data == "sub_menu_game_status":
        pass
    elif callback.data == "sub_menu_games_projects":
        pass
    elif callback.data == "sub_menu_donate":
        pass
    elif callback.data == "sub_menu_change_personal":
        handle_change_creds(callback.message)
    elif callback.data == "sub_menu_honorary_donor":
        pass
    else:
        return
