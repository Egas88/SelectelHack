import requests
from bot import bot

def handle_blood_stations_list(message):
    if message.text == "/view":
        url = 'https://hackaton.donorsearch.org/api/blood_stations/'
        params = {'blood_group': 'o_plus', 'city_id': get_city_id_by_name("Москва")}

        response = requests.get(url=url, params=params)

        parsed = response.json()
        #print(parsed["count"])
        #print(parsed["results"])

        blood_station_ids = [value["id"] for value in parsed["results"]]
        print(blood_station_ids)

        print_blood_stations_cards(message.from_user.id, blood_station_ids)
    else:
        raise Exception("Non valid message")

def print_blood_stations_cards(user_id, blood_station_ids):
    for blood_station_id in blood_station_ids:
        url = 'https://hackaton.donorsearch.org/api/blood_stations/{}/'

        response = requests.get(url=url.format(blood_station_id))
        result = response.json()
        title = result["title"]
        bot.send_message(user_id, title)
