import requests

def handle_blood_stations_list(bot, message):
    if message.text == "/viewBloodStations":
        response = requests.get('https://hackaton.donorsearch.org/api/blood_stations/')
        parsed = response.json()
        print(parsed["count"])
        print(parsed["results"])

        bot.send_message(message.chat.id, "Смотри логи е")

