import requests
from telebot import types
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from api import API_REGIONS, API_CITIES
from bot import bot
from cities.cities import get_city_id_by_name

@bot.callback_query_handler(func=lambda call: call.data.startswith('blood_station_region'))
def select_bs_region(call: CallbackQuery):
    if call.data.startswith("blood_station_region_page"):
        page = int(call.data.split('-')[1])
        markup = create_bs_regions_markup(page=page)
        bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region-"):
        region_id = call.data.split('-')[1]
        markup = create_bs_cities_markup(region_id)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region_city_page"):
        region_id = call.data.split('-')[1]
        page = int(call.data.split('-')[2])
        markup = create_bs_cities_markup(region_id, page=page)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region_city-"):
        city_id = call.data.split('-')[1]
        print_blood_stations_needs_cards(call.message.chat.id, get_blood_stations_with_needs_by_city_id(city_id))


def create_bs_regions_markup(page=1, per_page=10):
    responce = requests.get(f"{API_REGIONS}", params={"country": "1"}).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for region in responce[start:end]:
        markup.add(InlineKeyboardButton(region["title"], callback_data=f"blood_station_region-{region['id']}"))

    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'blood_station_region_page-{page - 1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'blood_station_region_page-{page + 1}'))
    if row:
        markup.row(*row)

    markup.row(InlineKeyboardButton('↩️ Назад в меню', callback_data='change_go_back'))
    return markup


def create_bs_cities_markup(region_id, page=1, per_page=10):
    responce = requests.get(f"{API_CITIES}", params={"country": "1", "region": f"{region_id}"}).json()
    responce = responce["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for city in responce[start:end]:
        markup.add(InlineKeyboardButton(city["title"], callback_data=f"blood_station_region_city-{city['id']}"))

    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'blood_station_region_city_page-{region_id}-{page - 1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'blood_station_region_city_page-{region_id}-{page + 1}'))
    if row:
        markup.row(*row)

    markup.add(InlineKeyboardButton("Назад к регионам", callback_data="blood_station_region_back_to_regions"))
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))
    return markup

def handle_test(message):
    markup = create_bs_regions_markup()
    bot.edit_message_text(text="Выберите регион: ", chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

# def create_bs_regions_markup(page=1, per_page=10):
#     responce = requests.get(f"{API_REGIONS}", params={"country": "1"}).json()
#     responce = responce["results"]
#     markup = InlineKeyboardMarkup()
#     total_pages = len(responce) // per_page + (1 if len(responce) % per_page > 0 else 0)
#     start = (page - 1) * per_page
#     end = start + per_page
#     for region in responce[start:end]:
#         markup.add(InlineKeyboardButton(region["title"], callback_data=f"blood_station_region-{region['id']}"))
#
#     row = []
#     if page > 1:
#         row.append(InlineKeyboardButton('⬅️', callback_data=f'blood_station_region_page-{page - 1}'))
#     if page < total_pages:
#         row.append(InlineKeyboardButton('➡️', callback_data=f'blood_station_region_page-{page + 1}'))
#     if row:
#         markup.row(*row)
#
#     markup.row(InlineKeyboardButton('↩️ Назад в меню', callback_data='change_go_back'))
#     return markup

# def handle_blood_stations_need_list(message, city_id):
#     # asfd

def get_blood_stations_with_needs_by_city_id(city_id):
    url = 'https://hackaton.donorsearch.org/api/needs'
    params = {"city_id": city_id}
    response = requests.get(url, params=params)

    response_json_result = response.json()["results"]
    result = []
    for response in response_json_result:
        cur_city_id = response["city_id"]
        if int(cur_city_id) == int(city_id):
            result.append(response)
    return result

def print_blood_stations_needs_cards(user_id, allowed_blood_stations_need):
    global cur_page_num
    global pages
    global message_id
    global pages_amount

    pages = []
    message_id = ''
    cur_page_num = 0
    pages_amount = 0

    if len(allowed_blood_stations_need) == 0:
        print("SAFASF")
    else:
        elements_in_page = 1

        allowed_bs_len = len(allowed_blood_stations_need)
        pages_amount = (allowed_bs_len // elements_in_page)
        if allowed_bs_len % 2 != 0 and allowed_bs_len != 1:
            pages_amount += 1

        for page_i in range(0, pages_amount):
            curPageText = ""
            newPage = []
            curPageText += """🩸 <b>Нуждающиеся пункты сбора крови</b>\n"""
            for i in range(0, elements_in_page):
                title = "\n" + "🏥 " + "<u>" + allowed_blood_stations_need[page_i + i]["title"] + "</u>"
                curPageText += title + "\n\n"

                o_plus = allowed_blood_stations_need[page_i + i]["o_plus"]
                o_plus_text = "O(+) \'Первая положительная\'"
                o_minus = allowed_blood_stations_need[page_i + i]["o_minus"]
                o_minus_text = "O(-) \'Первая отрицательная\'"
                a_plus = allowed_blood_stations_need[page_i + i]["a_plus"]
                a_plus_text = "A(+) \'Вторая положительная\'"
                a_minus = allowed_blood_stations_need[page_i + i]["a_minus"]
                a_minus_text = "A(-) \'Вторая отрицательная\'"
                b_plus = allowed_blood_stations_need[page_i + i]["b_plus"]
                b_plus_text = "B(+) \'Третья положительная\'"
                b_minus = allowed_blood_stations_need[page_i + i]["b_minus"]
                b_minus_text = "B(-) \'Третья отрицательная\'"
                ab_plus = allowed_blood_stations_need[page_i + i]["ab_plus"]
                ab_plus_text = "AB(+) \'Четвертая положительная\'"
                ab_minus = allowed_blood_stations_need[page_i + i]["ab_minus"]
                ab_minus_text = "AB(-) \'Четвертая отрицательная\'"

                if o_plus == "need":
                    curPageText += get_need_group_text(o_plus_text)
                else:
                    curPageText += get_no_need_group_text(o_plus_text)
                if o_minus == "need":
                    curPageText += get_need_group_text(o_minus_text)
                else:
                    curPageText += get_no_need_group_text(o_minus_text)
                curPageText += "\n"
                if a_plus == "need":
                    curPageText += get_need_group_text(a_plus_text)
                else:
                    curPageText += get_no_need_group_text(a_plus_text)
                if a_minus == "need":
                    curPageText += get_need_group_text(a_minus_text)
                else:
                    curPageText += get_no_need_group_text(a_minus_text)
                curPageText += "\n"
                if b_plus == "need":
                    curPageText += get_need_group_text(b_plus_text)
                else:
                    curPageText += get_no_need_group_text(b_plus_text)
                if b_minus == "need":
                    curPageText += get_need_group_text(b_minus_text)
                else:
                    curPageText += get_no_need_group_text(b_minus_text)
                curPageText += "\n"
                if ab_plus == "need":
                    curPageText += get_need_group_text(ab_plus_text)
                else:
                    curPageText += get_no_need_group_text(ab_plus_text)
                if ab_minus == "need":
                    curPageText += get_need_group_text(ab_minus_text)
                else:
                    curPageText += get_no_need_group_text(ab_minus_text)
                curPageText += "\n"

                address = allowed_blood_stations_need[page_i + i]["address"]
                curPageText += "📍 Адрес учреждения:\n<code>{}</code>".format(address)
                site = allowed_blood_stations_need[page_i + i]["site"]
                curPageText += "\n💻 Сайт:\n{}".format(site)
                phones = [value["phone"] for value in allowed_blood_stations_need[page_i + i]["phone_numbers"]]
                curPageText += "\n📞 Телефоны:"
                for phone in phones:
                    curPageText += "\n<code>{}</code>".format(phone)
                worktime = allowed_blood_stations_need[page_i + i]["worktime"]
                curPageText += "\n⌚ Время работы:\n"
                if len(worktime) > 0:
                    curPageText += "<i>{}</i>\n".format(worktime)
                else:
                    curPageText += "не определено 😢\n"

            newPage.append(curPageText)
            pages.append(newPage)

        markup = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
        page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_go_right')
        page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_go_left')
        markup.add(page_go_left_button, page_go_right_button)
        markup.add(back_button)

        message = bot.send_message(user_id, form_page_text(pages[cur_page_num]), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        message_id = message.message_id

def form_page_text(page):
    global cur_page_num
    global pages_amount

    dop = f"\n\n<i>Страница {cur_page_num + 1} из {pages_amount}</i>"
    result = ""
    for el in page:
        result += el
    result += dop
    return result

pages = []
message_id = ''
cur_page_num = 0
pages_amount = 0
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_go_'))
def page_go_left_right_button_callback(callback):
    global cur_page_num
    global pages
    global message_id
    global pages_amount

    chat_id = callback.message.chat.id
    if callback.data == "page_go_right":
        if (cur_page_num + 1) < pages_amount:
            cur_page_num += 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=form_page_text(pages[cur_page_num]), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
    elif callback.data == "page_go_left":
        if cur_page_num > 0:
            cur_page_num -= 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=form_page_text(pages[cur_page_num]), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
    else:
        return

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
    for i, blood_station_id in enumerate(blood_station_ids):
        url = 'https://hackaton.donorsearch.org/api/blood_stations/{}/'
        response = requests.get(url=url.format(blood_station_id))

        current_message += "🏥 " + form_blood_station_details(response.json())
        if i == len(result_messages) - 1:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            markup.add(back_button)

            bot.send_message(user_id, current_message, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        else:
            bot.send_message(user_id, current_message, parse_mode="HTML")
        current_message = ""


def form_blood_station_details(result_json):
    result_message = ""
    result_message += result_json["title"]
    result_message += "\nТелефон Центра крови:\n"
    result_message += "<code>" + result_json["phones"] + "</code>"

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
