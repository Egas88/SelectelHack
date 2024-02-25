import re

import requests
from telebot import types

from bot import bot

pages = []
message_id = ''
cur_page_num = 0
pages_amount = 0
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_event_go_'))
def page_go_left_right_button_callback(callback):
    global cur_page_num
    global pages
    global message_id
    global pages_amount

    chat_id = callback.message.chat.id
    if callback.data == "page_event_go_right":
        if (cur_page_num + 1) < pages_amount:
            cur_page_num += 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_event_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_event_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_id, parse_mode="HTML", text=form_page_text(pages[cur_page_num]), reply_markup=markup, disable_web_page_preview=True)
    elif callback.data == "page_event_go_left":
        if cur_page_num > 0:
            cur_page_num -= 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_event_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_event_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_id, parse_mode="HTML", text=form_page_text(pages[cur_page_num]), reply_markup=markup, disable_web_page_preview=True)
    else:
        return

def form_page_text(page):
    global cur_page_num
    global pages_amount

    dop = f"\n\nСтраница {cur_page_num + 1} из {pages_amount}"
    result = ""
    for el in page:
        result += el
    result += dop
    return result

def handle_events(message):
    url = "https://hackaton.donorsearch.org/api/events/"
    response = requests.get(url=url)

    response_json_result = response.json()["results"]

    global pages
    global pages_amount
    global message_id
    global cur_page_num

    pages = []
    message_id = ''
    cur_page_num = 0
    pages_amount = 0

    message_id = message.message_id

    el_in_page = 4
    pages_amount = len(response_json_result) // el_in_page
    if len(response_json_result) % el_in_page != 0:
        pages_amount += 1
    for i in range(0, pages_amount):
        new_page = ""
        for j in range(0, el_in_page):
            cur_res = response_json_result[i + j]
            new_page += "📢 " + cur_res["name"] + "\n\n"
            new_page += "⌚️Дата проведения: " + "<u>" + str(cur_res["start_date"])[:10] + " - " + str(cur_res["end_date"])[:10] + "</u>" + "\n"

            place = cur_res["blood_station"]
            if place is not None:
                new_page += "📍 Место проведения мероприятия: " + place["address"] + "\n"
            new_page += "\n"
            description = cur_res["description"]
            new_description = re.sub("(<br>|</br>|<p>|</p>|&mdash|\t\|)", "", description)
            new_description = new_description.replace("|", "")
            if new_description == "":
                new_description = "Здесь могло бы быть описание вашего мероприятия!"
            new_page += "<i>" + new_description + "</i>"
            new_page += "\n\n\n"
        pages.append(new_page)

    markup = types.InlineKeyboardMarkup(row_width=2)
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_event_go_right')
    page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_event_go_left')
    markup.add(page_go_left_button, page_go_right_button)
    markup.add(back_button)
    # bot.edit_message_text(chat_id=user_id, message_id=orig_message_id, text=form_page_text(pages[cur_page_num]),
    #                       reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

    bot.edit_message_text(text=form_page_text(pages[0]), chat_id=message.chat.id, parse_mode="HTML", message_id=message.message_id, reply_markup=markup, disable_web_page_preview=True)
    print()
