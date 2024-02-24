import requests
from telebot import types
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from api import API_REGIONS, API_CITIES
from bot import bot
from cities.cities import get_city_id_by_name

o_plus_text = "O(+) \'Первая положительная\'"
o_minus_text = "O(-) \'Первая отрицательная\'"
a_plus_text = "A(+) \'Вторая положительная\'"
a_minus_text = "A(-) \'Вторая отрицательная\'"
b_plus_text = "B(+) \'Третья положительная\'"
b_minus_text = "B(-) \'Третья отрицательная\'"
ab_plus_text = "AB(+) \'Четвертая положительная\'"
ab_minus_text = "AB(-) \'Четвертая отрицательная\'"

bt_dict = {'o_plus': o_plus_text, 'o_minus': o_minus_text, 'a_plus': a_plus_text, 'a_minus': a_plus_text, 'b_plus': b_plus_text, 'b_minus': b_minus_text, 'ab_plus': ab_plus_text, 'ab_minus': ab_minus_text}

def handle_bs_need(message):
    global pages
    pages = []
    global message_id
    message_id = ''
    global cur_page_num
    cur_page_num = 0
    global pages_amount
    pages_amount = 0

    markup = create_bs_need_regions_markup()
    bot.edit_message_text(text="Выберите регион: ", chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

# def handle_bs_list(message):
#     markup = create_bs_regions_markup()
#     bot.edit_message_text(text="Выберите регион: ", chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)

def handle_blood_stations_list(message):
    global pages_bs_list
    pages_bs_list = []
    global pages_bs_amount
    pages_bs_amount = 0
    global message_bs_id
    message_bs_id = ''
    global cur_page_bs_num
    cur_page_bs_num = 0

    markup = create_bs_regions_markup()
    bot.edit_message_text(text="Выберите регион: ", chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('blood_station_region'))
def select_bs_need_region(call: CallbackQuery):
    if call.data.startswith("blood_station_region_page"):
        page = int(call.data.split('-')[1])
        markup = create_bs_need_regions_markup(page=page)
        bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region-"):
        region_id = call.data.split('-')[1]
        markup = create_bs_need_cities_markup(region_id)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region_city_page"):
        region_id = call.data.split('-')[1]
        page = int(call.data.split('-')[2])
        markup = create_bs_need_cities_markup(region_id, page=page)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_region_city-"):
        city_id = call.data.split('-')[1]
        print_blood_stations_needs_cards(call.message.chat.id, call.message.message_id, get_blood_stations_with_needs_by_city_id(city_id))

def print_bs_list_by_city_id_and_bt(message, city_id, blood_type):
    url = 'https://hackaton.donorsearch.org/api/blood_stations/'
    params = {'blood_group': blood_type, 'city_id': city_id}
    response = requests.get(url=url, params=params)

    blood_stations = response.json()["results"]

    allowed_blood_stations = []
    for j in range(0, len(blood_stations)):
        if int(blood_stations[j]["city_id"]) is int(city_id):
            allowed_blood_stations.append(blood_stations[j])

    blood_station_ids = [value["id"] for value in allowed_blood_stations]

    print_blood_stations_cards(message, blood_station_ids, allowed_blood_stations[0]["city"]["title"], blood_type)

city_id_for_bt = 0
@bot.callback_query_handler(func=lambda call: call.data.startswith('blood_type_'))
def selected_blood_type(call: CallbackQuery):
    global city_id_for_bt
    if call.data.startswith("blood_type_o_plus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'o_plus')
    elif call.data.startswith("blood_type_o_minus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'o_minus')
    elif call.data.startswith("blood_type_a_plus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'a_plus')
    elif call.data.startswith("blood_type_a_minus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'a_minus')
    elif call.data.startswith("blood_type_b_plus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'b_plus')
    elif call.data.startswith("blood_type_b_minus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'b_minus')
    elif call.data.startswith("blood_type_ab_plus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'ab_plus')
    elif call.data.startswith("blood_type_ab_minus"):
        print_bs_list_by_city_id_and_bt(call.message, city_id_for_bt, 'ab_minus')

@bot.callback_query_handler(func=lambda call: call.data.startswith('blood_station_list_region'))
def select_bs_list_region(call: CallbackQuery):
    global city_id_for_bt

    if call.data.startswith("blood_station_list_region_page"):
        page = int(call.data.split('-')[1])
        markup = create_bs_regions_markup(page=page)
        bot.edit_message_text(text="Выберите регион: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_list_region-"):
        region_id = call.data.split('-')[1]
        markup = create_bs_cities_markup(region_id)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_list_region_city_page"):
        region_id = call.data.split('-')[1]
        page = int(call.data.split('-')[2])
        markup = create_bs_cities_markup(region_id, page=page)
        bot.edit_message_text(text="Выберите город: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith("blood_station_list_region_city-"):
        city_id_for_bt = call.data.split('-')[1]

        # print_blood_stations_needs_cards(call.message.chat.id, get_blood_stations_with_needs_by_city_id(city_id))
        # запросить группу КРОВЫ

        markup = types.InlineKeyboardMarkup(row_width=1)
        o_plus_btn = types.InlineKeyboardButton(o_plus_text, callback_data='blood_type_o_plus')
        o_minus_btn = types.InlineKeyboardButton(o_minus_text, callback_data='blood_type_o_minus')

        a_plus_btn = types.InlineKeyboardButton(a_plus_text, callback_data='blood_type_a_plus')
        a_minus_btn = types.InlineKeyboardButton(a_minus_text, callback_data='blood_type_a_minus')

        b_plus_btn = types.InlineKeyboardButton(b_plus_text, callback_data='blood_type_b_plus')
        b_minus_btn = types.InlineKeyboardButton(b_minus_text, callback_data='blood_type_b_minus')

        ab_plus_btn = types.InlineKeyboardButton(ab_plus_text, callback_data='blood_type_ab_plus')
        ab_minus_btn = types.InlineKeyboardButton(ab_minus_text, callback_data='blood_type_ab_minus')

        markup.add(o_plus_btn)
        markup.add(o_minus_btn)

        markup.add(a_plus_btn)
        markup.add(a_minus_btn)

        markup.add(b_plus_btn)
        markup.add(b_minus_btn)

        markup.add(ab_plus_btn)
        markup.add(ab_minus_btn)

        bot.edit_message_text(text="Выберите вашу группу крови: ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def create_bs_regions_markup(page=1, per_page=10):
    response = requests.get(f"{API_REGIONS}", params={"country": "1"}).json()
    response = response["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(response) // per_page + (1 if len(response) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for region in response[start:end]:
        markup.add(InlineKeyboardButton(region["title"], callback_data=f"blood_station_list_region-{region['id']}"))

    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'blood_station_list_region_page-{page - 1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'blood_station_list_region_page-{page + 1}'))
    if row:
        markup.row(*row)

    markup.row(InlineKeyboardButton('↩️ Назад в меню', callback_data='change_go_back'))
    return markup


def create_bs_cities_markup(region_id, page=1, per_page=10):
    response = requests.get(f"{API_CITIES}", params={"country": "1", "region": f"{region_id}"}).json()
    response = response["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(response) // per_page + (1 if len(response) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for city in response[start:end]:
        markup.add(InlineKeyboardButton(city["title"], callback_data=f"blood_station_list_region_city-{city['id']}"))

    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'blood_station_list_region_city_page-{region_id}-{page - 1}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'blood_station_list_region_city_page-{region_id}-{page + 1}'))
    if row:
        markup.row(*row)

    markup.add(InlineKeyboardButton("Назад к регионам", callback_data="blood_station_list_region_back_to_regions"))
    markup.row(InlineKeyboardButton('↩️  Назад в меню ', callback_data='change_go_back'))
    return markup

def create_bs_need_regions_markup(page=1, per_page=10):
    response = requests.get(f"{API_REGIONS}", params={"country": "1"}).json()
    response = response["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(response) // per_page + (1 if len(response) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for region in response[start:end]:
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


def create_bs_need_cities_markup(region_id, page=1, per_page=10):
    response = requests.get(f"{API_CITIES}", params={"country": "1", "region": f"{region_id}"}).json()
    response = response["results"]
    markup = InlineKeyboardMarkup()
    total_pages = len(response) // per_page + (1 if len(response) % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    for city in response[start:end]:
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

def print_blood_stations_needs_cards(user_id, orig_message_id, allowed_blood_stations_need):
    global cur_page_num
    global pages
    global message_id
    global pages_amount

    pages = []
    message_id = ''
    cur_page_num = 0
    pages_amount = 0

    if len(allowed_blood_stations_need) == 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
        markup.add(back_button)
        bot.edit_message_text(chat_id=user_id, message_id=orig_message_id,
                              text="😢 <b>К сожалению ничего не найдено</b>",
                              reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
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
                if page_i + i + 1 > len(allowed_blood_stations_need):
                    break
                else:
                    title = "\n" + "🏥 " + "<u>" + allowed_blood_stations_need[page_i + i]["title"] + "</u>"
                    curPageText += title + "\n\n"

                    o_plus = allowed_blood_stations_need[page_i + i]["o_plus"]
                    o_minus = allowed_blood_stations_need[page_i + i]["o_minus"]
                    a_plus = allowed_blood_stations_need[page_i + i]["a_plus"]
                    a_minus = allowed_blood_stations_need[page_i + i]["a_minus"]
                    b_plus = allowed_blood_stations_need[page_i + i]["b_plus"]
                    b_minus = allowed_blood_stations_need[page_i + i]["b_minus"]
                    ab_plus = allowed_blood_stations_need[page_i + i]["ab_plus"]
                    ab_minus = allowed_blood_stations_need[page_i + i]["ab_minus"]

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
        bot.edit_message_text(chat_id=user_id, message_id=orig_message_id, text=form_page_text(pages[cur_page_num]),
                              reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

        message_id = orig_message_id

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


def print_blood_stations_cards(message, blood_station_ids, city_name, blood_type):
    global pages_bs_list
    global message_bs_id
    global pages_bs_amount

    global bt_dict

    message_bs_id = message.message_id

    title = f"📲 По вашему запросу город - <u>{city_name}</u>, группа крови <u>{bt_dict[blood_type]}</u> найдены следующие результаты:\n"

    result_messages = []
    current_message = ""
    for i, blood_station_id in enumerate(blood_station_ids):
        url = 'https://hackaton.donorsearch.org/api/blood_stations/{}/'
        response = requests.get(url=url.format(blood_station_id))

        current_message += "🏥 " + form_blood_station_details(response.json())
        result_messages.append(current_message)
        current_message = ""

    elements_in_page = 4

    allowed_bs_len = len(result_messages)
    pages_bs_amount = (allowed_bs_len // elements_in_page)
    if allowed_bs_len % 2 != 0 and allowed_bs_len != 1:
        pages_bs_amount += 1

    for i in range(0, pages_bs_amount):
        newPage = "" + title + "\n"

        for j in range(0, elements_in_page):
            if i + j + 1 > len(result_messages):
                break
            else:
                newPage += result_messages[i + j]
        pages_bs_list.append(newPage)

    markup = types.InlineKeyboardMarkup(row_width=2)
    back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')

    if len(pages_bs_list) == 0:
        markup.add(back_button)
        bot.edit_message_text(text="😢 <b>К сожалению ничего не найдено</b>", chat_id=message.chat.id,
                              message_id=message.message_id, reply_markup=markup, parse_mode="HTML")
    else:
        page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_bs_go_right')
        page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_bs_go_left')
        markup.add(page_go_left_button, page_go_right_button)
        markup.add(back_button)
        bot.edit_message_text(text=form_bs_page_text(pages_bs_list[0]), chat_id=message.chat.id,
                              message_id=message.message_id, reply_markup=markup, parse_mode="HTML")

pages_bs_list = []
pages_bs_amount = 0
message_bs_id = ''
cur_page_bs_num = 0
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_bs_go_'))
def page_bs_go_left_right_button_callback(callback):
    global cur_page_bs_num
    global pages_bs_list
    global message_bs_id
    global pages_bs_amount

    chat_id = callback.message.chat.id
    if callback.data == "page_bs_go_right":
        if (cur_page_bs_num + 1) < pages_bs_amount:
            cur_page_bs_num += 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_bs_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_bs_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_bs_id, text=form_bs_page_text(pages_bs_list[cur_page_bs_num]), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
    elif callback.data == "page_bs_go_left":
        if cur_page_bs_num > 0:
            cur_page_bs_num -= 1

            markup = types.InlineKeyboardMarkup(row_width=2)
            back_button = types.InlineKeyboardButton('↩️ Назад ', callback_data='change_go_back')
            page_go_right_button = types.InlineKeyboardButton('➡️', callback_data='page_bs_go_right')
            page_go_left_button = types.InlineKeyboardButton('⬅️', callback_data='page_bs_go_left')
            markup.add(page_go_left_button, page_go_right_button)
            markup.add(back_button)

            bot.edit_message_text(chat_id=chat_id, message_id=message_bs_id, text=form_bs_page_text(pages_bs_list[cur_page_bs_num]), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
    else:
        return

def form_bs_page_text(page):
    global cur_page_bs_num
    global pages_bs_amount

    dop = f"\n\n<i>Страница {cur_page_bs_num + 1} из {pages_bs_amount}</i>"
    result = ""
    for el in page:
        result += el
    result += dop
    return result

def get_need_group_text(group_need):
    return "🟢 " + group_need + "\n"

def get_no_need_group_text(group_no_need):
    return "🔴 " + group_no_need + "\n"

def form_blood_station_details(result_json):
    result_message = ""
    result_message += result_json["title"] + "\n"
    if len(result_json["phone_numbers"]) != 0:
        result_message += "Телефон Центра крови:\n"
        for phone in result_json["phone_numbers"]:
            result_message += "<code>" + phone["phone"] + "</code>\n"

    site_link = result_json["parser_url"]
    if site_link is not None:
        result_message += "Ссылка на сайт:\n"
        result_message += site_link

    result_message += "\n"
    return result_message

def get_blood_stations_needs_by_id(blood_station_id):
    url = 'https://hackaton.donorsearch.org/api/needs/{}'
    response = requests.get(url.format(blood_station_id))

    response_json = response.json()
    return response_json
