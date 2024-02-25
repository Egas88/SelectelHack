from telebot import types
from telebot.types import InputMediaPhoto
import requests

from auth_register import users
from auth_register.change_creds.change_creds import handle_change_creds

from blood_station.blood_station import handle_blood_stations_list, handle_bs_need
from bot import bot
from donation.donation import handle_donation_adding
from donation.donation_planning import handle_donation_planning
from donation.guide import handle_blood_donation_guide
from donation.get_donations import handle_see_donations
from events.events import handle_events


def handle_donations_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_donation_button = types.InlineKeyboardButton('Добавить донацию', callback_data='sub_menu_add_donation')
    plan_donation_button = types.InlineKeyboardButton('Запланировать донацию', callback_data='sub_menu_plan_donation')
    see_planned_donations_button = types.InlineKeyboardButton('Посмотреть запланированные донации', callback_data='sub_menu_see_planned_donations')
    see_donations_button = types.InlineKeyboardButton('Посмотреть добавленные донации', callback_data='sub_menu_see_donations')
    blood_donation_guide_button = types.InlineKeyboardButton('Памятка по подготовке к сдачи крови', callback_data='sub_menu_blood_donation_guide')

    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b> Донации 💉 </b>
    
🩸 Здесь вы можете добавить, запланировать и запросить донацию. 

📃 Также вы можете получить памятку по подготовке к сдаче крови! 

    """
    markup.add(add_donation_button, see_donations_button , plan_donation_button, see_planned_donations_button, blood_donation_guide_button, back_button)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text = msg_txt, reply_markup=markup, parse_mode="HTML")

def handle_blood_centers_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    blood_stations_button = types.InlineKeyboardButton('Запросить карточки центров крови',
                                                       callback_data='sub_menu_blood_stations')
    address_needs_button = types.InlineKeyboardButton('Запросить адресные потребности',
                                                      callback_data='sub_menu_address_needs')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
🩸 <b>Центры крови</b>
    
🗺️ Здесь вы можете узнать расположение центров крови. 

📍  Также можете найти близжайшитй к Вам центр! 

    """
    markup.add(blood_stations_button, address_needs_button, back_button)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
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
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")



def handle_personal_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    donate_button = types.InlineKeyboardButton('Сделать пожертвование проекту', callback_data='sub_menu_donate')
    change_personal = types.InlineKeyboardButton('Сменить личные данные', callback_data='sub_menu_change_personal')
    honorary_donor_button = types.InlineKeyboardButton('Запросить статус до почетного донора',
                                                       callback_data='sub_menu_honorary_donor')
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    msg_txt = """
    <b>⚙️ Личные настройки</b>
    
💵 Поддержите наш проект и сделайте мир лучше

✍️ Измените личные данные

🏆 Станьте почетным донором! 

    """
    markup.add(donate_button, change_personal, honorary_donor_button, back_button)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")


def handle_articles_menu(message):
    users.is_aricles = True
    markup = types.InlineKeyboardMarkup(row_width=1)
    guide_link = types.InlineKeyboardButton('📜 Все последние новости ',
                                            url="https://journal.donorsearch.org/")
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    last_news = get_last_news()
    keys = list(last_news.keys())
    values = list(last_news.values())

    if len(last_news) < 4:
        return
    msg_txt = f"""
📜 Последние новости из нашего журнала 
⭐ {keys[0]}
⭐ {keys[1]}
⭐ {keys[2]}
⭐ {keys[3]}
        
💉 Для получения самой свежей информации о донорстве и новейших открытиях в мире медицины и гематологии перейдите на наш ресурс! 

        """

    markup.add(guide_link, back_button)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    #bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    media_group = []
    first = True
    for img in values:
        photo_response = requests.get(img).content
        if first:
            first = False
            media_group.append(InputMediaPhoto(photo_response, caption=msg_txt))
        else:
            media_group.append(InputMediaPhoto(photo_response))

    message_to_save = bot.send_media_group(message.chat.id, media=media_group)
    users.old_man_pic_delete_message = message_to_save
    bot.send_message(message.chat.id, "Изучить эти новости и просмотреть ещё больше новостей Вы можете получить нажав по кнопке ниже", reply_markup=markup, parse_mode="HTML")

def get_last_news():
    from bs4 import BeautifulSoup

    url = 'https://journal.donorsearch.org/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        h3_tags_class_h2 = soup.find_all('h3', class_='t-entry-title h2')
        h3_tags_class_h4 = soup.find_all('h3', class_='t-entry-title h4')

        news = []

        for tag in h3_tags_class_h2:
            news.append(tag.text.strip())

        for tag in h3_tags_class_h4:
            news.append(tag.text.strip())

        news_guid_mapping = {}

        div_tags_class_async_done = soup.find_all('div', class_='t-background-cover adaptive-async')
        for i, tag in enumerate(div_tags_class_async_done):
            data_guid = tag.get('data-guid')
            news_guid_mapping[news[i]] = data_guid

        return news_guid_mapping





@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_menu_'))
def process_register_step(callback):
    if callback.data == "sub_menu_add_donation":
        handle_donation_adding(callback.message)
    elif callback.data == "sub_menu_plan_donation":
        handle_donation_planning(callback.message)
    elif callback.data == "sub_menu_see_planned_donations":
        handle_see_donations(callback.message, True)
    elif callback.data == "sub_menu_see_donations":
        handle_see_donations(callback.message, False)
    elif callback.data == "sub_menu_blood_donation_guide":
        handle_blood_donation_guide(callback.message)
    elif callback.data == "sub_menu_blood_stations":
        handle_blood_stations_list(callback.message)
    elif callback.data == "sub_menu_address_needs":
        handle_bs_need(callback.message)
    elif callback.data == "sub_menu_game_status":
        pass
    elif callback.data == "sub_menu_games_projects":
        handle_events(callback.message)
    elif callback.data == "sub_menu_donate":
        pass
    elif callback.data == "sub_menu_change_personal":
        handle_change_creds(callback.message)
    elif callback.data == "sub_menu_honorary_donor":
        pass
    else:
        return
