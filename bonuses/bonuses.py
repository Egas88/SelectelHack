import requests
import re

from telebot import types

from bot import bot
from api import *
from auth_register.users import users_dict
from menu.menu import handle_menu

bonus_ids = []

def handle_view_bonuses_list(message):
    url = API_BONUSES
    response = requests.get(url)

    print(response.json())
    response_json = response.json()
    bonuses = response_json["results"]

    result = ""
    for bonus in bonuses:
        bonus_id = bonus["id"]

        details_json = get_info_by_bonus_id(bonus_id)

        #Test getting feedback
        #bonus_feedback_details = leave_feedback_by_bonus_id(message.chat.id, bonus_id, "Comment", 5)

        result += form_html_message_by_bonus(details_json)

    user_id = message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
    markup.add(back_button)

    bot.send_message(user_id, result, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

def form_html_message_by_bonus(bonus_details_json):
    bonus_name = bonus_details_json["bonus_name"]
    bonus_partner = bonus_details_json["partner_name"]
    bonus_expired = bonus_details_json["date_validity"]
    bonus_description = format_description(bonus_details_json["bonus_description"])
    bonus_partner_url = bonus_details_json["partner_url"]
    bonus_partner_promocode = bonus_details_json["promocode"]

    if bonus_partner_promocode is None:
        bonus_partner_promocode = "BLANK"

    msgFinal = f"""📌 <b>Предложение: <u>{bonus_name}</u> от {bonus_partner} <u>действует до {bonus_expired}</u></b>

{bonus_description}

🥁<i>Промокод</i> <code>{bonus_partner_promocode}</code>

<i>Подробности по ссылке</i> {bonus_partner_url}

"""

    #Всунуть в HTML
    #bonus_image_url = bonus["bonus_image"]

    return msgFinal

def format_description(description):
    description_without_tags = re.sub("(<br>|</br>|<p>|</p>|&mdash|\t|;)", "", description)

    array_description = description_without_tags.split(".")
    return array_description[0] + "."

def get_info_by_bonus_id(bonus_id):
    url = API_BONUSES_ID
    response = requests.get(url.format(bonus_id))

    response_json = response.json()
    print(response_json)
    return response_json

def leave_feedback_by_bonus_id(user_id, bonus_id, comment, rating):
    url = API_BONUSES_ID_FEEDBACK
    response = requests.patch(url.format(bonus_id), data={"rating": rating, "comment": comment}, auth=(users_dict[user_id]["username"], users_dict[user_id]["password"]))

    response_json = response.json()
    print(response_json)
    return response_json
