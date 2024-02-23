import requests
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import calendar
import datetime
from bot import bot
import re

months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

request_data = {}

def handle_donation_adding(message):
    select_donation_type(message)


def select_donation_type(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    whole_blood_btn = types.KeyboardButton('Цельная кровь')
    plasma_btn = types.KeyboardButton('Плазма')
    platelets_btn = types.KeyboardButton('Тромбоциты')
    red_blood_btn = types.KeyboardButton('Эритроциты')
    granulocytes_btn = types.KeyboardButton('Гранулоциты')
    markup.add(whole_blood_btn, plasma_btn, platelets_btn, red_blood_btn, granulocytes_btn)
    bot.send_message(message.from_user.id, "Выберите тип донации", reply_markup=markup)
    bot.register_next_step_handler(message, get_calendar)


# Дальше блга нет, тут функции календаря чисто
def create_calendar(year, month):
    
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(f"{months[month-1]} {year}", callback_data="donation_month_year"))
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
                row.append(InlineKeyboardButton(str(day), callback_data=f"donation_data_{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"))
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
        month_button = InlineKeyboardButton(months[i-1], callback_data=f"donation_month-{i}")
        if i % 3 == 1:
            month_row = []
        month_row.append(month_button)
        if i % 3 == 0:
            markup.row(*month_row)
    
    # markup.row(InlineKeyboardButton("Сегодня", callback_data=f"month-{month}-year-{year}"))
    
    return markup


def get_calendar(message):
    now = datetime.datetime.now()
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Выберите дату: ", reply_markup=markup)
    markup = create_calendar(now.year, now.month)
    bot.send_message(message.chat.id, "Календарь:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_data_'))
def data_select(call: CallbackQuery):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Вы выбрали " + call.data[14:],
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_month'))
def select_month(call):
    if call.data == "donation_month_year":
        now = datetime.datetime.now()
        markup = create_month_year_selection(now.year, now.month)
        bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("donation_month"):
        month = int(call.data.split('-')[1])
        now = datetime.datetime.now()
        markup = create_calendar(now.year, month)
        bot.edit_message_text(f"Выбран месяц: {months[month-1]}", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('donation_year'))
def select_year(call):
    year = int(call.data.split('-')[1])
    now = datetime.datetime.now()
    markup = create_month_year_selection(year, now.month)
    bot.edit_message_text("Выберите месяц и год:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



        