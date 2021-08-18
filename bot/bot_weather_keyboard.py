from telebot.types import ReplyKeyboardMarkup


def kb_lvl_1_city(cities):
    keyboard = ReplyKeyboardMarkup(row_width=2)
    to_add_btn = []
    for i in cities:
        to_add_btn.append(i)
    keyboard.add(*to_add_btn)
    keyboard.resize_keyboard = True

    return keyboard


def kb_lvl_2():
    kb_lvl = {
        'Сейчас': 'Сейчас',
        'На будущее': 'На будущее'
    }
    keyboard = ReplyKeyboardMarkup(row_width=2)
    to_add_btn = []
    for i in kb_lvl:
        to_add_btn.append(i)
    keyboard.add(*to_add_btn)
    keyboard.add('Назад')
    keyboard.resize_keyboard = True

    return keyboard
