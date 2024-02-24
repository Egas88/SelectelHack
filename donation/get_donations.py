from bot import bot
from api import API_DONATION_PLAN, API_DONATIONS
from auth_register.users import get_username, get_password
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from menu.menu_handlers import handle_donations_menu
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
            markup.add(InlineKeyboardButton(text = f"Вы запланировали посещение на {station["plan_date"]}. {f"На выездную акцию в {station["city"]["title"]}" if station["is_out"] == "true" else f"В центре крови {station['blood_station']['title']}" if station["blood_station"] is not None else ""}", callback_data=f"donations_list_cell-{station['id']}"))
        else:
            markup.add(InlineKeyboardButton(text = f"Вы были записаны на {station["donate_at"]}. {f"На выездную акцию в {station["city"]["title"]}" if station["is_out"] == "true" else f"В центре крови {station['blood_station']['title']}" if station["blood_station"] is not None else ""}", callback_data=f"donations_list_cell-{station['id']}"))
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donations_list_page-{page-1}-{is_plan}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donations_list_page-{page+1}-{is_plan}'))
    if row:
        markup.row(*row)

    markup.row(InlineKeyboardButton('↩️  Назад к выбору ', callback_data='donations_list_go_to_menu'))
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))

    return markup


def create_delete_change_donations_markup(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text = "Удалить донацию", callback_data="get_donations_delete"))
    markup.add(InlineKeyboardButton(text = "Изменить донацию", callback_data="get_donations_change"))
    markup.add(InlineKeyboardButton(text = "Посмотреть донации", callback_data="get_donations_see"))
    markup.add(InlineKeyboardButton(text = "↩️   Назад в меню", callback_data="change_go_back"))
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите действие c донацией",
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
    elif call.data.startswith('donations_list_go_to_menu'):
        handle_donations_menu(call.message)
    elif call.data.startswith('donations_list_cell'):
        donation_id = call.data.split('-')[1]
        markup = InlineKeyboardMarkup()






