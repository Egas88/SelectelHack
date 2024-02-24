import requests
from telebot import types
from telebot.types import CallbackQuery

from bot import bot
from cities.cities import get_city_id_by_name

# def process_blood_stations_step(message):
from donation.donation import create_regions_markup, create_cities_markup, choose_blood_station
from menu.menu import handle_menu


# @bot.callback_query_handler(func=lambda call: call.data.startswith('donation_region'))
# def select_region(call: CallbackQuery):
#     if call.data.startswith("donation_region_page"):
#         page = int(call.data.split('-')[1])
#         markup = create_regions_markup(page=page)
#         bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
#     elif call.data.startswith("donation_region-"):
#         region_id = call.data.split('-')[1]
#         markup = create_cities_markup(region_id)
#         bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
#     elif call.data.startswith("donation_region_city_page"):
#         region_id = call.data.split('-')[1]
#         page = int(call.data.split('-')[2])
#         markup = create_cities_markup(region_id, page=page)
#         bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
#     elif call.data.startswith("donation_region_city-"):
#         city_id = call.data.split('-')[1]
#         #request_data["city_id"] = city_id
#         #displayed_data["city"] = requests.get(f"https://hackaton.donorsearch.org{API_CITIES_ID.format(id=city_id)}").json()["results"]["title"]
#         #print(displayed_data["city"])
#         message = call.message
#         choose_blood_station(message)
#     elif call.data.startswith("donation_region_back_to_regions"):
#         markup = create_regions_markup()
#         bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

def handle_test(callback):
    page = int(callback.data.split('-')[1])
    markup = create_regions_markup(page=page)
    bot.edit_message_text(text="Выберите регион: ", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

def handle_blood_stations_need_list(message):
    city_id = get_city_id_by_name("Москва")
    blood_stations_need = get_blood_stations_with_needs_by_city_id(city_id)["results"]

    allowed_blood_stations_need = []
    for i in range(0, len(blood_stations_need)):
        current_city_id = int(blood_stations_need[i]["city_id"])
        if current_city_id is city_id:
            allowed_blood_stations_need.append(blood_stations_need[i])
    print_blood_stations_needs_cards(message.chat.id, allowed_blood_stations_need)

def get_blood_stations_with_needs_by_city_id(city_id):
    url = 'https://hackaton.donorsearch.org/api/needs'
    params = {"city_id": city_id}
    response = requests.get(url, params=params)

    response_json = response.json()
    print()
    return response_json

def print_blood_stations_needs_cards(user_id, allowed_blood_stations_need):
    if len(allowed_blood_stations_need) == 0:
        print("SAFASF")
    else:
        main_title = """🩸 Нуждающиеся пункты сбора крови"""
        bot.send_message(user_id, main_title, parse_mode="HTML", disable_web_page_preview=True)
        for i, allowed in enumerate(allowed_blood_stations_need):
            curText = ""
            title = "\n" + "🏥 " + "<u>" + allowed["title"] + "</u>"
            curText += title + "\n\n"

            o_plus = allowed["o_plus"]
            o_plus_text = "O(+) \'Первая положительная\'"
            o_minus = allowed["o_minus"]
            o_minus_text = "O(-) \'Первая отрицательная\'"
            a_plus = allowed["a_plus"]
            a_plus_text = "A(+) \'Вторая положительная\'"
            a_minus = allowed["a_minus"]
            a_minus_text = "A(-) \'Вторая отрицательная\'"
            b_plus = allowed["b_plus"]
            b_plus_text = "B(+) \'Третья положительная\'"
            b_minus = allowed["b_minus"]
            b_minus_text = "B(-) \'Третья отрицательная\'"
            ab_plus = allowed["ab_plus"]
            ab_plus_text = "AB(+) \'Четвертая положительная\'"
            ab_minus = allowed["ab_minus"]
            ab_minus_text = "AB(-) \'Четвертая отрицательная\'"

            if o_plus == "need":
                curText += get_need_group_text(o_plus_text)
            else:
                curText += get_no_need_group_text(o_plus_text)
            if o_minus == "need":
                curText += get_need_group_text(o_minus_text)
            else:
                curText += get_no_need_group_text(o_minus_text)
            curText += "\n"
            if a_plus == "need":
                curText += get_need_group_text(a_plus_text)
            else:
                curText += get_no_need_group_text(a_plus_text)
            if a_minus == "need":
                curText += get_need_group_text(a_minus_text)
            else:
                curText += get_no_need_group_text(a_minus_text)
            curText += "\n"
            if b_plus == "need":
                curText += get_need_group_text(b_plus_text)
            else:
                curText += get_no_need_group_text(b_plus_text)
            if b_minus == "need":
                curText += get_need_group_text(b_minus_text)
            else:
                curText += get_no_need_group_text(b_minus_text)
            curText += "\n"
            if ab_plus == "need":
                curText += get_need_group_text(ab_plus_text)
            else:
                curText += get_no_need_group_text(ab_plus_text)
            if ab_minus == "need":
                curText += get_need_group_text(ab_minus_text)
            else:
                curText += get_no_need_group_text(ab_minus_text)
            curText += "\n"

            address = allowed["address"]
            curText += "📍 Адрес учреждения:\n<code>{}</code>".format(address)
            site = allowed["site"]
            curText += "\n💻 Сайт:\n{}".format(site)
            phones = [value["phone"] for value in allowed["phone_numbers"]]
            curText += "\n📞 Телефоны:"
            for phone in phones:
                curText += "\n<code>{}</code>".format(phone)
            worktime = allowed["worktime"]
            curText += "\n⌚ Время работы:\n"
            if len(worktime) > 0:
                curText += "<i>{}</i>".format(worktime)
            else:
                curText += "не определено 😢"

            if i == len(allowed_blood_stations_need) - 1:
                markup = types.InlineKeyboardMarkup(row_width=1)
                back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
                markup.add(back_button)

                bot.send_message(user_id, curText, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
            else:
                bot.send_message(user_id, curText, parse_mode="HTML", disable_web_page_preview=True)

def get_need_group_text(group_need):
    return "🟢 " + group_need + "\n"

def get_no_need_group_text(group_no_need):
    return "🔴 " + group_no_need + "\n"

def handle_blood_stations_list(message):
    blood_group = "o_plus"
    city_id = get_city_id_by_name("Санкт-Петербург")
    url = 'https://hackaton.donorsearch.org/api/blood_stations/'
    params = {'blood_group': 'o_plus', 'city_id': city_id}
    response = requests.get(url=url, params=params)

    blood_stations = response.json()["results"]

    allowed_blood_stations = []
    for j in range(0, len(blood_stations)):
        if blood_stations[j]["city_id"] is city_id:
            allowed_blood_stations.append(blood_stations[j])

    blood_station_ids = [value["id"] for value in allowed_blood_stations]

    # Check BS needs
    # for blood_station_id in blood_station_ids:
    #     x = get_blood_stations_needs_by_id(blood_station_id)
    # y = get_blood_stations_with_needs_by_city_id(city_id)

    print(blood_station_ids)

    #print_general_info(message.chat.id, city_id, blood_group)
    print_blood_stations_cards(message.chat.id, blood_station_ids)

def print_general_info(user_id, city_id, blood_group):
    msgResult = """
    """

    bot.send_message(user_id, msgResult, parse_mode="HTML")

def print_blood_stations_cards(user_id, blood_station_ids):
    result_messages = []
    current_message = ""
    i = 0
    for blood_station_id in blood_station_ids:
        i += 1
        url = 'https://hackaton.donorsearch.org/api/blood_stations/{}/'
        response = requests.get(url=url.format(blood_station_id))

        current_message += str(i) + ". " + form_blood_station_details(response.json())
        if len(current_message) > 2000:
            result_messages.append(current_message)
            current_message = ""

    result_messages.append(current_message)

    for i, result_message in enumerate(result_messages):
        if i == len(result_messages) - 1:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            markup.add(back_button)

            bot.send_message(user_id, result_message, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        else:
            bot.send_message(user_id, result_message)



def form_blood_station_details(result_json):
    result_message = ""
    result_message += result_json["title"]
    result_message += "\nТелефон Центра крови:\n"
    result_message += result_json["phones"]

    site_link = result_json["parser_url"]
    if site_link is not None:
        result_message += "\nСсылка на сайт:\n"
        result_message += site_link

    result_message += "\n\n"
    return result_message

def get_blood_stations_needs_by_id(blood_station_id):
    url = 'https://hackaton.donorsearch.org/api/needs/{}'
    response = requests.get(url.format(blood_station_id))

    response_json = response.json()
    print()
    return response_json

# def get_bold_text(text):
#     bold = "<b>{}</b>"
#     return bold.format(text)
