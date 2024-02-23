import requests
from bot import bot

def handle_blood_stations_list(message):
    if message.text == "/viewBloodStations":
        response = requests.get('https://hackaton.donorsearch.org/api/blood_stations/')
        parsed = response.json()
        print(parsed["count"])
        print(parsed["results"])
        print(message.from_user.id)

        bot.send_message(message.from_user.id, "Смотри логи е")
    else:
        print("ПНХ")
