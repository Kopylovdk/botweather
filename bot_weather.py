import threading
import telebot
from telebot import types

from bot.bot_weather_keyboard import kb_lvl_1_city, kb_lvl_2
from bot.bot_weather_const import city_dict, WEATHER_APP_ID, TELEGRAM_BOT_TOKEN, ADMIN_ID
from bot.bot_weather_get_weather import get_city_one_call

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Главное меню. Если вы не нашли нужный город - напишите боту '
                                      '"Новый город - название города" и бот перенаправит сообщение администратору '
                                      'для добавления', reply_markup=kb_lvl_1_city(city_dict))


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text in city_dict:
        city_name = message.text
        selected_city = city_dict[city_name]
        message = bot.reply_to(message, "Прогноз на сейчас или на будущее?", reply_markup=kb_lvl_2())
        bot.register_next_step_handler(message, forecast_select, selected_city, city_name)
    elif 'НОВЫЙ ГОРОД' in message.text.upper():
        bot.send_message(ADMIN_ID, f'Пользователь с ID {message.from_user.id},\n'
                                   f'Логин: {message.from_user.username}\n'
                                   f'ФИО: {message.from_user.first_name} {message.from_user.last_name}\n'
                                   f'просит добавить город: {message.text}')
    else:
        bot.send_message(message.chat.id, 'Такой команды не существует. Возврат в главное меню',
                         reply_markup=kb_lvl_1_city(city_dict))


def forecast_select(message, selected_city, city_name):
    if message.text == 'Сейчас':
        bot.send_message(message.chat.id, 'Ожидайте ответ, ваш запрос в очереди.',
                         reply_markup=types.ReplyKeyboardRemove())
        # data, img_path = get_city_one_call(selected_city, WEATHER_APP_ID, 'current', city_name)
        data = get_city_one_call(selected_city, WEATHER_APP_ID, 'current', city_name)
        # if data and img_path:
        #     with open(img_path, 'rb') as to_send:
        #         bot.send_photo(message.chat.id, to_send,
        #                        caption=f"{data['Дата'][0]} {data['Город'][0]}\n{data['Восход/закат'][0]}\n"
        #                                f"{data['Температура'][0]}\n"
        #                                f"{data['Влажность'][0]}\n{data['Давление'][0]}\n{data['УФ индекс'][0]}\n"
        #                                f"{data['Ветер'][0]}",
        #                        reply_markup=kb_lvl_1_city(city_dict))

        if data:
            bot.send_message(message.chat.id, f"{data['Дата'][0]} {data['Город'][0]}\n{data['Восход/закат'][0]}\n"
                                              f"{data['Температура'][0]}\n"
                                              f"{data['Влажность'][0]}\n{data['Давление'][0]}\n{data['УФ индекс'][0]}\n"
                                              f"{data['Ветер'][0]}",
                             reply_markup=kb_lvl_1_city(city_dict))
        else:
            bot.send_message(message.chat.id, 'Время ожидания ответа от сервиса погоды истекло. ПОвторите попытку.',
                             reply_markup=kb_lvl_1_city(city_dict))
    elif message.text == 'На будущее':
        bot.send_message(message.chat.id, 'Ожидайте ответ, ваш запрос в очереди.',
                         reply_markup=types.ReplyKeyboardRemove())
        data = get_city_one_call(selected_city, WEATHER_APP_ID, 'daily', city_name)
        if data:
            for i in range(len(data['Дата'])):
                bot.send_message(message.chat.id, f"{data['Дата'][i]}, {data['Город'][0]}, {data['Восход/закат'][i]}\n"
                                                  f"{data['Температура'][i]}\n"
                                                  f"{data['Влажность'][i]}, {data['Давление'][i]}, {data['УФ индекс'][i]}\n"
                                                  f"{data['Ветер'][i]}",
                                 reply_markup=kb_lvl_1_city(city_dict))
        else:
            bot.send_message(message.chat.id, 'Время ожидания ответа от сервиса погоды истекло. ПОвторите попытку.',
                             reply_markup=kb_lvl_1_city(city_dict))
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=kb_lvl_1_city(city_dict))
    else:
        bot.send_message(message.chat.id, 'Такой команды не существует. Возврат в главное меню',
                         reply_markup=kb_lvl_1_city(city_dict))


threading.Thread(bot.polling(none_stop=True, interval=0), name='telegram_thread_v2')
