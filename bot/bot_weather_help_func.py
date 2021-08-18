import requests


def get_city_id(city_name, app_id):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
    data = res.json()
    result = []
    for i in data['list']:
        result.append(f"ID = {i['id']}, Название: {i['name']}, Координаты: {i['coord']}, Страна: {i['sys']['country']}")
    return result


def get_wind_direction(deg):
    result = ''
    wind = ['северный ', 'северо-восточный', 'восточный', 'юго-восточный',
            'южный', 'юго-западный', 'западный', 'северо-западный']
    for i in range(0, 8):
        step = 45.
        min_w = i * step - 45 / 2.
        max_w = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if min_w <= deg <= max_w:
            result = wind[i]
            break
    return result
