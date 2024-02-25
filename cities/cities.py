import requests

def get_city_id_by_name(city_name):
    url = 'https://hackaton.donorsearch.org/api/cities/'
    response = requests.get(url=url)
    parsed = response.json()

    all_cities = parsed["results"]

    for city in all_cities:
        if city["title"] == city_name:
            return city["id"]

    raise Exception("Where is no such city")
