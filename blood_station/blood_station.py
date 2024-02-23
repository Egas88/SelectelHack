import requests
from telebot import types
from bot import bot
from cities.cities import get_city_id_by_name

# def process_blood_stations_step(message):


def handle_blood_stations_list(message):
    # markup = types.ReplyKeyboardMarkup(row_width=1)
    # email_btn = types.KeyboardButton('По Email')
    # phone_btn = types.KeyboardButton('По номеру телефона')
    # markup.add(email_btn, phone_btn)
    # bot.register_next_step_handler(message, process_blood_stations_step)

    if message.text == "/view":
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
        print(blood_station_ids)

        print_blood_stations_cards(message.from_user.id, blood_station_ids)
    else:
        raise Exception("Non valid message")


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

    for result_message in result_messages:
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

# def get_bold_text(text):
#     bold = "<b>{}</b>"
#     return bold.format(text)
