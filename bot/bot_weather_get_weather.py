import requests
import datetime
import sys
import os

sys.path.append(os.path.join(sys.path[0], 'bot'))

from bot_weather_help_func import get_wind_direction, get_city_id
from bot_weather_const import IMG_PATH, city_dict, HPA


# def get_city_weather(city, app_id):
#     res = requests.get("http://api.openweathermap.org/data/2.5/weather",
#                        params={'id': city['id'], 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
#     data = res.json()
#     weather_image = requests.get(f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
#
#     with open(f'{IMG_PATH}{data["weather"][0]["icon"]}.png', 'wb') as img:
#         img.write(weather_image.content)
#         img_path = f'{IMG_PATH}{data["weather"][0]["icon"]}.png'
#     if data['main']['temp_min'] == data['main']['temp_max']:
#         text = f"Город: {data['name']}\n" \
#                f"Восход: {datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}, " \
#                f"Закат: {datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}\n" \
#                f"Температура: {data['main']['temp_min']}\N{DEGREE SIGN}C, {data['weather'][0]['description']}, " \
#                f"ощущается как: {data['main']['feels_like']}\N{DEGREE SIGN}C\n" \
#                f"Влажность: {data['main']['humidity']}% Давление: {data['main']['pressure']}hPa " \
#                f"Ветер {get_wind_direction(data['wind']['deg'])}, {data['wind']['speed']} м/с"
#     else:
#         text = f"Город: {data['name']}\n" \
#                f"Восход: {datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}, " \
#                f"Закат: {datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}\n" \
#                f"Температура: от {data['main']['temp_min']}\N{DEGREE SIGN}C " \
#                f"до {data['main']['temp_max']}\N{DEGREE SIGN}C, {data['weather'][0]['description']}, " \
#                f"ощущается как: {data['main']['feels_like']}\N{DEGREE SIGN}C\n" \
#                f"Влажность: {data['main']['humidity']}% Давление: {data['main']['pressure']}hPa " \
#                f"Ветер {get_wind_direction(data['wind']['deg'])}, {data['wind']['speed']} м/с"
#     return text, img_path


# def get_city_forecast(city, app_id):
#     res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
#                        params={'id': city['id'], 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
#     data = res.json()
#     text = [f"Город: {data['city']['name']}. "
#             f"Восход: {datetime.datetime.fromtimestamp(data['city']['sunrise']).strftime('%H:%M:%S')} "
#             f"Закат: {datetime.datetime.fromtimestamp(data['city']['sunset']).strftime('%H:%M:%S')}\n"]
#     for i in range(len(data['list']) - 30):
#         text.append(f"{data['list'][i]['dt_txt'][5:16]},"
#                     f" {'{0:+3.0f}'.format(data['list'][i]['main']['temp'])}\N{DEGREE SIGN}C "
#                     f"{data['list'][i]['weather'][0]['description']},"
#                     f" Ветер:{'{0:2.0f}'.format(data['list'][i]['wind']['speed'])} м/с, направление: "
#                     f"{get_wind_direction(data['list'][i]['wind']['deg'])}\n")
#     return text


def get_city_one_call(city, app_id, time, city_name):
    for i in range(10):
        try:
            result = requests.get("https://api.openweathermap.org/data/2.5/onecall",
                                  params={'lat': city['lat'], 'lon': city['lon'], 'units': 'metric', 'lang': 'ru',
                                          'APPID': app_id}, timeout=(4, 4))
            data = result.json()
            table = {'Дата': [],
                     'Город': [f"{city_name}"],
                     'Восход/закат': [],
                     'Температура': [],
                     'Влажность': [],
                     'Давление': [],
                     'Ветер': [],
                     'УФ индекс': [],
                     }
            if time == 'daily':
                for day in data[time]:
                    table['Дата'].append(datetime.datetime.fromtimestamp(day['dt']).strftime('%d.%m'))
                    table['Восход/закат'].append(
                        f"восход {datetime.datetime.fromtimestamp(day['sunrise']).strftime('%H:%M:%S')}, "
                        f"закат {datetime.datetime.fromtimestamp(day['sunset']).strftime('%H:%M:%S')}")
                    table['Температура'].append(
                        f"{day['weather'][0]['description']}. Температора:\n"
                        f"Ночью {day['temp']['night']}\N{DEGREE SIGN}C, "
                        f"ощущается как {day['feels_like']['night']}\N{DEGREE SIGN}C\n"
                        f"Утром {day['temp']['morn']}\N{DEGREE SIGN}C, "
                        f"ощущается как {day['feels_like']['morn']}\N{DEGREE SIGN}C\n"
                        f"Днем {day['temp']['day']}\N{DEGREE SIGN}C, "
                        f"ощущается как {day['feels_like']['day']}\N{DEGREE SIGN}C\n"
                        f"Вечером {day['temp']['eve']}\N{DEGREE SIGN}C, "
                        f"ощущается как {day['feels_like']['eve']}\N{DEGREE SIGN}C")
                    table['Влажность'].append(f"влажность {day['humidity']}%")
                    table['Давление'].append(f"давление {round(day['pressure'] * HPA, 2)}ммРС")
                    table['Ветер'].append(
                        f"ветер {get_wind_direction(day['wind_deg'])}, {day['wind_speed']} м/с")
                    table['УФ индекс'].append(f"УФ индекс {day['uvi']}")
                return table
            elif time == 'current':
                # weather_image = requests.get(f"http://openweathermap.org/img/wn/{data[time]['weather'][0][
                # 'icon']}@2x.png") with open(f'{IMG_PATH}{data[time]["weather"][0]["icon"]}.png', 'wb') as img:
                # img.write(weather_image.content) img_path = f'{IMG_PATH}{data[time]["weather"][0]["icon"]}.png'
                table['Дата'].append(datetime.datetime.fromtimestamp(data[time]['dt']).strftime('%H:%M:%S'))
                table['Восход/закат'].append(
                    f"восход {datetime.datetime.fromtimestamp(data[time]['sunrise']).strftime('%H:%M:%S')},\n"
                    f"закат {datetime.datetime.fromtimestamp(data[time]['sunset']).strftime('%H:%M:%S')}")
                table['Температура'].append(
                    f"{data[time]['weather'][0]['description']},\nтемпература "
                    f"{data[time]['temp']}\N{DEGREE SIGN}C,\n"
                    f"ощущается как {data[time]['feels_like']}\N{DEGREE SIGN}C")
                table['Влажность'].append(f"влажность {data[time]['humidity']}%")
                table['Давление'].append(f"давление {round(data[time]['pressure'] * HPA, 2)}ммРС")
                table['Ветер'].append(
                    f"ветер {get_wind_direction(data[time]['wind_deg'])}, {data[time]['wind_speed']} м/с")
                table['УФ индекс'].append(f"УФ индекс {data[time]['uvi']}")
                return table  # , img_path
        except requests.ReadTimeout:
            continue

# print(get_city_forecast(524901, "742f5a88c7d36f8ae9ec784de5dfdfd9"))
# print(get_city_weather(524901, "742f5a88c7d36f8ae9ec784de5dfdfd9"))
# print(get_city_one_call(city_dict['Москва'], "742f5a88c7d36f8ae9ec784de5dfdfd9", 'current', 'Москва'))
# print(get_city_id('Санкт-Петербург', "742f5a88c7d36f8ae9ec784de5dfdfd9"))
