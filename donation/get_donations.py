from bot import bot
from api import API_DONATION_PLAN, API_DONATIONS
from auth_register.users import get_username, get_password
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telebot import types
from api import API_DONATION_PLAN_ID, API_DONATIONS_ID
import requests


def create_donations_markup(message, is_plan, page = 1, per_page = 10):
    responce = ""
    if is_plan:
        responce = requests.get(API_DONATION_PLAN, auth=(get_username(message.chat.id), get_password(message.chat.id))).json()
    else:
        responce = requests.get(API_DONATIONS, auth=(get_username(message.chat.id), get_password(message.chat.id))).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page

    for station in responce[start:end]:
        if is_plan:
            plan_date = station["plan_date"]
            station_city_title = station["city"]["title"]
            station_bs_title = station['blood_station']['title']
            markup.add(InlineKeyboardButton(text = f"Вы запланировали посещение на {plan_date}. {f'На выездную акцию в {station_city_title}' if station['is_out'] == 'true' else f'В центре крови {station_bs_title}' if station['blood_station'] is not None else ''}", callback_data=f"donations_list_cell-{station['id']}-{is_plan}"))
        else:
            station_donate_at = station["donate_at"]
            station_city_title = station["city"]["title"]
            station_bs_title = station['blood_station']['title']
            markup.add(InlineKeyboardButton(text = f"Вы были записаны на {station_donate_at}. {f'На выездную акцию в {station_city_title}' if station['is_out'] == 'true' else f'В центре крови {station_bs_title}' if station['blood_station'] is not None else ''}", callback_data=f"donations_list_cell-{station['id']}-{is_plan}"))
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donations_list_page-{page-1}-{is_plan}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donations_list_page-{page+1}-{is_plan}'))
    if row:
        markup.row(*row)

    markup.row(InlineKeyboardButton('↩️  Назад к выбору ', callback_data="menu_donations"))
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))

    return markup


def create_change_donations_markup(message, donation_id, is_plan):
    markup = InlineKeyboardMarkup(row_width=2)
    delete_donation_btn = types.InlineKeyboardButton(text = "Удалить донацию", callback_data=f"get_donations-{donation_id}-delete-{is_plan}")
    #change_donation_btn = types.InlineKeyboardButton(text = "Изменить донацию", callback_data=f"get_donations-{donation_id}-change-{is_plan}")
    choose_donations_btn = types.InlineKeyboardButton(text = "↩️  Вернуться к выбору донации", callback_data=f"get_donations_back-{is_plan}")
    back_to_menu_btn = types.InlineKeyboardButton(text = "↩️   Назад в меню", callback_data="change_go_back")
    markup.add(delete_donation_btn, choose_donations_btn, back_to_menu_btn)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите действие c донацией:",
        reply_markup=markup
    )


def handle_see_donations(message, is_plan):
    markup = create_donations_markup(message, is_plan)
    text = ""
    if is_plan:
        text = "Запланированные донации"
    else:
        text= "Добавленные донации"
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('donations_list'))
def list_donations(call: CallbackQuery):
    if call.data.startswith('donations_list_page'):
        page = int(call.data.split('-')[1])
        is_plan = call.data.split('-')[2] == "True"
        markup = create_donations_markup(call.message, is_plan, page=page)
        text = ""
        if is_plan:
            text = "Запланированные донации"
        else:
            text= "Добавленные донации"
        bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith('donations_list_cell'):
        donation_id = call.data.split('-')[1]
        is_plan = call.data.split('-')[2] == "True"
        create_change_donations_markup(call.message, donation_id, is_plan)
        


@bot.callback_query_handler(func=lambda call: call.data.startswith('get_donations'))
def change_donation(call: CallbackQuery):
    if call.data.startswith("get_donations_back"):
        is_plan = call.data.split('-')[2] == "True"
        handle_see_donations(call.message, is_plan)
    elif call.data.startswith("get_donations"):
        donation_id = call.data.split('-')[1]
        is_plan = call.data.split('-')[3] == "True"
        if call.data.split('-')[2] == "delete":
            if is_plan:
                requests.delete(API_DONATION_PLAN_ID.format(donation_id), auth=(get_username(call.message.chat.id), get_password(call.message.chat.id)))
                markup = create_donations_markup(call.message,is_plan)
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Заявка была удалена!",
                    reply_markup=markup
                )
            else:
                requests.delete(API_DONATIONS_ID.format(donation_id), auth=(get_username(call.message.chat.id), get_password(call.message.chat.id)))
                markup = create_donations_markup(call.message, is_plan)
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Заявка была удалена!",
                    reply_markup=markup
                )
        # elif call.data.split('-')[2] == "change":
        #     change_donation(call.message, donation_id)