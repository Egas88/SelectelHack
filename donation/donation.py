import requests
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import calendar
import datetime
from bot import bot
from api import API_REGIONS
import re

months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

request_data = {}

def handle_donation_adding(message):
    select_donation_type(message)


def select_donation_type(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Цельная кровь", callback_data="donation_blood_type-blood"), InlineKeyboardButton("Плазма", callback_data="donation_blood_type-plasma"))
    markup.row(InlineKeyboardButton("Тромбоциты", callback_data="donation_blood_type-platelets"), InlineKeyboardButton("Эритроциты", callback_data="donation_blood_type-erythrocytes"))
    markup.row(InlineKeyboardButton("Гранулоциты", callback_data="donation_blood_type-leukocytes"))
    bot.send_message(message.chat.id, "Выберите тип крови:", reply_markup=markup)


def choose_payment_type(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    free = types.InlineKeyboardButton("Безвозмездно", callback_data="donation_payment_type-free")
    payed = types.InlineKeyboardButton("Платно", callback_data="donation_payment_type-payed")
    markup.add(free, payed)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text = """
        <b> Безвозмездно </b>
Питание или компенсация питания
(5% МРОТ порядка 700-1500 ₽. Учитывается при получении звания Почетного донора.)

<b> Платно </b>
Деньги или социальная поддержка. Не учитывается при получении звания почетного донора

Выберите тип донации: 

    """, 
        reply_markup=markup,
        parse_mode="HTML",
    )


def choose_is_out(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    false = types.InlineKeyboardButton("Стационарный пункт", callback_data="donation_is_out-false")
    true = types.InlineKeyboardButton("Выездная акция", callback_data="donation_is_out-true")
    markup.add(false, true)
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=message.message_id, 
        text = """
        <b> Стационарый пункт </b>
Центр крови или станция переливания в вашем городе

<b>Выездная акция</b>
День донора, выезды в ВУЗы, передвижные мобильные бригады

Выберите место сдачи: 

    """, 
        reply_markup=markup,
        parse_mode="HTML",
    )


def choose_region(message):
    responce = requests.get(f"https://hackaton.donorsearch.org{API_REGIONS}", params={"Country": "1"}).json()
    responce = responce["results"]
    
    print(responce["results"])




# Дальше блга нет, тут функции календаря чисто
def create_calendar(year, month):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(f"{months[month-1]} {year}", callback_data=f"donation_select_year-{month}-{year}"))
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
                row.append(InlineKeyboardButton(str(day), callback_data=f"donation_data_{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"))
        markup.row(*row)
    
    return markup


def create_month_year_selection(year, month):
    markup = InlineKeyboardMarkup()
    year_row = []
    year_row.append(InlineKeyboardButton("<<", callback_data=f"donation_year-{year-1}"))
    year_row.append(InlineKeyboardButton(f"{year}", callback_data="ignore"))
    year_row.append(InlineKeyboardButton(">>", callback_data=f"donation_year-{year+1}"))
    markup.row(*year_row)
    
    for i in range(1, 13):
        month_button = InlineKeyboardButton(months[i-1], callback_data=f"donation_select_month-{i}-{year}")
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_data_'))
def data_select(call: CallbackQuery):
    request_data["plan_date"] = call.data[14:]
    print(request_data["plan_date"])
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Вы выбрали " + call.data[14:],
    )
    message = call.message
    choose_payment_type(message)



@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_select'))
def select_month(call: CallbackQuery):
    if call.data.startswith("donation_select_year"):
        month = int(call.data.split('-')[1])
        year = int(call.data.split('-')[2])
        markup = create_month_year_selection(year, month)
        bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_select_month"):
        month = int(call.data.split('-')[1])
        year = int(call.data.split('-')[2])
        markup = create_calendar(year, month)
        bot.edit_message_text(f"Выбран месяц: {months[month-1]}", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_year'))
def select_year(call: CallbackQuery):
    year = int(call.data.split('-')[1])
    now = datetime.datetime.now()
    markup = create_month_year_selection(year, now.month)
    bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_blood_type'))
def select_blood_type(call: CallbackQuery):
        blood_type = call.data.split('-')[1]
        request_data["blood_type"] = blood_type
        print(request_data["blood_type"])
        message = call.message
        get_calendar(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_payment_type'))
def select_payment_type(call: CallbackQuery):
    payment_type = call.data.split('-')[1]
    request_data["payment_type"] = payment_type
    print(request_data["payment_type"])
    message = call.message
    choose_is_out(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_is_out'))
def select_is_out(call: CallbackQuery):
    is_out = call.data.split('-')[1]
    request_data["is_out"] = is_out
    print(request_data["is_out"])
    message = call.message
    choose_region(message)
