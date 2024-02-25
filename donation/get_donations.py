from bot import bot
from api import API_DONATION_PLAN, API_DONATIONS
from auth_register.users import get_username, get_password
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
            markup.add(InlineKeyboardButton(text = f"Вы запланировали посещение на {station['plan_date']}.", callback_data=f"ignore"))
        else:
            markup.add(InlineKeyboardButton(text = f"Вы были записаны на {station['donate_at']}.", callback_data=f"ignore"))
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'donations_list_page-{page-1}-{is_plan}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'donations_list_page-{page+1}-{is_plan}'))
    if row:
        markup.row(*row)
    
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))

    return markup


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


@bot.callback_query_handler(func=lambda call: call.data.startswith('donations_list_page'))
def list_donations(call: CallbackQuery):
    page = int(call.data.split('-')[1])
    is_plan = call.data.split('-')[2] == "True"
    markup = create_donations_markup(call.message, is_plan, page=page)
    text = ""
    if is_plan:
        text = "Запланированные донации"
    else:
        text= "Добавленные донации"
    bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)






