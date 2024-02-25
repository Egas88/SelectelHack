import requests
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import calendar
import datetime
from bot import bot
from api import API_REGIONS, API_CITIES, API_BLOOD_STATIONS, API_DONATION_PLAN
from auth_register.users import get_username, get_password
from notification_manager.notifications import add_notification_on_donation_plan
from menu.menu import handle_menu


blood_types = {"blood": "Цельная кровь", "plasma": "Плазма", "platelets": "Тромбоциты", "erythrocytes": "Эритроциты", "leukocytes": "Гранулоциты"}
request_data = {}
months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
displayed_data = {}

def handle_donation_planning(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Цельная кровь", callback_data="donation_planning_blood_type-blood"), InlineKeyboardButton("Плазма", callback_data="donation_planning_blood_type-plasma"))
    markup.row(InlineKeyboardButton("Тромбоциты", callback_data="donation_planning_blood_type-platelets"), InlineKeyboardButton("Эритроциты", callback_data="donation_planning_blood_type-erythrocytes"))
    markup.row(InlineKeyboardButton("Гранулоциты", callback_data="donation_planning_blood_type-leukocytes"))
    markup.row(InlineKeyboardButton('↩️ Назад в меню ', callback_data='change_go_back'))
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="🩸 Выберите тип крови:", 
        reply_markup=markup
    )


def choose_payment_type(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    free = types.InlineKeyboardButton("Безвозмездно", callback_data="donation_planning_payment_type-free")
    payed = types.InlineKeyboardButton("Платно", callback_data="donation_planning_payment_type-payed")
    back_button = types.InlineKeyboardButton('↩️ Назад в меню ', callback_data='change_go_back')
    markup.add(free, payed, back_button)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text = """
        <b>🤲 Безвозмездно </b>
Питание или компенсация питания
(5% МРОТ порядка 700-1500 ₽. Учитывается при получении звания Почетного донора.)

<b>💵 Платно </b>
Деньги или социальная поддержка. Не учитывается при получении звания почетного донора

Выберите тип донации: 

    """, 
        reply_markup=markup,
        parse_mode="HTML",
    )


def choose_is_out(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    false = types.InlineKeyboardButton("Стационарный пункт", callback_data="donation_planning_is_out-false")
    true = types.InlineKeyboardButton("Выездная акция", callback_data="donation_planning_is_out-true")
    back_button = types.InlineKeyboardButton('↩️ Назад в меню ', callback_data='change_go_back')
    markup.add(false, true, back_button)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text = """
<b>🏥 Стационарый пункт </b>
Центр крови или станция переливания в вашем городе

<b>🚐 Выездная акция</b>
День донора, выезды в ВУЗы, передвижные мобильные бригады

Выберите место сдачи: 

    """, 
        reply_markup=markup,
        parse_mode="HTML",
    )


def create_regions_markup(page = 1, per_page = 10):
    responce = requests.get(f"{API_REGIONS}", params={"country": "1"}).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for region in responce[start:end]:
        markup.add(InlineKeyboardButton(region["title"], callback_data=f"donation_planning_region-{region['id']}"))
    
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donation_planning_region_page-{page-1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donation_planning_region_page-{page+1}'))
    if row:
        markup.row(*row)

    markup.row(InlineKeyboardButton('↩️ Назад в меню', callback_data='change_go_back'))
    return markup


def create_cities_markup(region_id, page = 1, per_page = 10):
    responce = requests.get(f"{API_CITIES}", params={"country": "1", "region": f"{region_id}"}).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for city in responce[start:end]:
        markup.add(InlineKeyboardButton(city["title"], callback_data=f"donation_planning_region_city-{city['id']}"))
    
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donation_planning_region_city_page-{region_id}-{page-1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donation_planning_region_city_page-{region_id}-{page+1}'))
    if row:
        markup.row(*row)
    
    markup.add(InlineKeyboardButton("Назад к регионам", callback_data="donation_planning_region_back_to_regions"))
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))
    return markup


def choose_region(message):
    markup = create_regions_markup()
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text="Выберите регион: ",
        reply_markup=markup
    )


def create_blood_stations_markup(page = 1, per_page = 10):
    responce = requests.get(f"{API_BLOOD_STATIONS}", params={"city_id": f"{request_data['city_id']}"}).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for station in responce[start:end]:
        markup.add(InlineKeyboardButton(station["title"], callback_data=f"donation_planning_blood_station-{station['id']}"))
    
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donation_planning_blood_station_page-{page-1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donation_planning_blood_station_page-{page+1}'))
    if row:
        markup.row(*row)
    
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))

    return markup


def choose_blood_station(message):
    markup = create_blood_stations_markup()
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите центр крови: ",
        reply_markup=markup
    )


def choose_is_need(message):
    markup = types.InlineKeyboardMarkup()
    send = types.InlineKeyboardButton("Отправить", callback_data="donation_planning_send-true")
    change = types.InlineKeyboardButton("Изменить данные", callback_data="donation_planning_send-false")
    back_button = types.InlineKeyboardButton('↩️ Назад в меню ', callback_data='change_go_back')
    markup.add(send, change, back_button)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=f"""
Вы выбрали следующие параметры:

<b>🩸Тип крови</b>
{displayed_data["blood_type"]}

<b>Дата</b>
{displayed_data["plan_date"]}

<b>💵Тип донации</b>
{displayed_data["payment_type"]}

<b>🚐Место сдачи</b>
{displayed_data["is_out"]}

<b>🏥Город</b>
{displayed_data["city"]}

{f'''<b>💉Центр крови</b>
{displayed_data["blood_station"]}''' if displayed_data["is_out"] == "false" else ""}
""",
        reply_markup=markup,
        parse_mode="HTML"
    )


def create_notification_message():
    return f"""Напомнаем вам о запланированной донации сегодня {f'''в {displayed_data["blood_station"]}''' if displayed_data["is_out"] == "false" else ""}"""


# Дальше бога нет, тут функции календаря чисто
def create_calendar(year, month):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(f"{months[month-1]} {year}", callback_data=f"donation_planning_select_year-{month}-{year}"))
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    row = [InlineKeyboardButton(day, callback_data='ignore') for day in days]
    markup.row(*row)

    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data='ignore'))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=f"donation_planning_data-{year}-{str(month).zfill(2)}-{str(day).zfill(2)}-{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"))
        markup.row(*row)
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))
    return markup


def create_month_year_selection(year, month):
    markup = InlineKeyboardMarkup()
    year_row = []
    year_row.append(InlineKeyboardButton("<<", callback_data=f"donation_planning_year-{year-1}"))
    year_row.append(InlineKeyboardButton(f"{year}", callback_data="ignore"))
    year_row.append(InlineKeyboardButton(">>", callback_data=f"donation_planning_year-{year+1}"))
    markup.row(*year_row)
    
    for i in range(1, 13):
        month_button = InlineKeyboardButton(months[i-1], callback_data=f"donation_planning_select_month-{i}-{year}")
        if i % 3 == 1:
            month_row = []
        month_row.append(month_button)
        if i % 3 == 0:
            markup.row(*month_row)

    return markup


def get_calendar(message):
    now = datetime.datetime.now()
    markup = create_calendar(now.year, now.month)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text="Выберите дату: ", 
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_blood_type'))
def select_blood_type(call: CallbackQuery):
        blood_type = call.data.split('-')[1]
        request_data["blood_class"] = blood_type
        displayed_data["blood_type"] = blood_types[blood_type]
        message = call.message
        get_calendar(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_data'))
def data_select(call: CallbackQuery):
    if datetime.datetime.now().date() > datetime.datetime(year=int(call.data.split('-')[1]), month=int(call.data.split('-')[2]), day=int(call.data.split('-')[3])).date():
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Планируемая дата не может быть раньше, чем сегодня. Выберите другую дату.",
            reply_markup=create_calendar(datetime.datetime.now().year, datetime.datetime.now().month),
        )
    else:
        request_data["plan_date"] = call.data.split('-')[1] + "-" + call.data.split('-')[2] + "-" + call.data.split('-')[3]
        date = call.data.split('-')[4]
        displayed_data["plan_date"] = date
        message = call.message
        choose_payment_type(message)



@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_select'))
def select_month(call: CallbackQuery):
    if call.data.startswith("donation_planning_select_year"):
        month = int(call.data.split('-')[1])
        year = int(call.data.split('-')[2])
        markup = create_month_year_selection(year, month)
        bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_planning_select_month"):
        month = int(call.data.split('-')[1])
        year = int(call.data.split('-')[2])
        markup = create_calendar(year, month)
        bot.edit_message_text(f"Выбран месяц: {months[month-1]}", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_year'))
def select_year(call: CallbackQuery):
    year = int(call.data.split('-')[1])
    now = datetime.datetime.now()
    markup = create_month_year_selection(year, now.month)
    bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_payment_type'))
def select_payment_type(call: CallbackQuery):
    payment_type = call.data.split('-')[1]
    request_data["payment_type"] = payment_type
    if payment_type == "free":
        displayed_data["payment_type"] = "Безвозмездно"
    else:
        displayed_data["payment_type"] = "Платно"
    message = call.message
    choose_is_out(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_is_out'))
def select_is_out(call: CallbackQuery):
    is_out = call.data.split('-')[1]
    request_data["is_out"] = is_out
    if is_out == "true":
        displayed_data["is_out"] = "Выездная акция"
    elif is_out == "false":
        displayed_data["is_out"] = "Стационарный пункт"
    message = call.message
    choose_region(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_region'))
def select_region(call: CallbackQuery):
    if call.data.startswith("donation_planning_region_page"):
        page = int(call.data.split('-')[1])
        markup = create_regions_markup(page=page)
        bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_planning_region-"):
        region_id = call.data.split('-')[1]
        markup = create_cities_markup(region_id)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_planning_region_city_page"):
        region_id = call.data.split('-')[1]
        page = int(call.data.split('-')[2])
        markup = create_cities_markup(region_id, page=page)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_planning_region_city-"):
        city_id = call.data.split('-')[1]
        request_data["city_id"] = city_id
        displayed_data["city"] = requests.get(f"{API_CITIES}{city_id}/").json()["title"]
        message = call.message
        if request_data["is_out"] == "true":
            choose_is_need(message)
        else:
            choose_blood_station(message)
    elif call.data.startswith("donation_planning_region_back_to_regions"):
        markup = create_regions_markup()
        bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_blood_station'))
def select_blood_station(call: CallbackQuery):
    if call.data.startswith("donation_planning_blood_station_page"):
        page = int(call.data.split('-')[1])
        markup = create_blood_stations_markup(page=page)
        bot.edit_message_text(text="Выберите центр крови: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_planning_blood_station-"):
        blood_station_id = call.data.split('-')[1]
        request_data["blood_station_id"] = blood_station_id
        displayed_data["blood_station"] = requests.get(f"{API_BLOOD_STATIONS}{blood_station_id}/").json()["title"]
        message = call.message
        choose_is_need(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_planning_send'))
def select_send_or_change(call: CallbackQuery):
    is_send = call.data.split('-')[1]
    if is_send == "true":
        request_data["status"] = "active"
        responce = requests.post(API_DONATION_PLAN, json=request_data, auth=(get_username(call.message.chat.id), get_password(call.message.chat.id)))
        add_notification_on_donation_plan(call.message.chat.id, request_data["date"], create_notification_message())
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Ваша заявка была отправлена!",
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Ваша заявка была отправлена!",
        )
        handle_menu(call.message)
    elif is_send == "false":
        handle_donation_planning(call.message)
