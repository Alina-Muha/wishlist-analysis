import telebot
from telebot import types
from src.steam_web_api_iteractions2 import main

bot = telebot.TeleBot('1486307406:AAFYJJHnIChyLvxpS_a9O0y7xumya1__-L8')


@bot.message_handler(commands=["start"])
def any_msg(message):
    bot.send_message(message.from_user.id, "Привет!")
    keyboard = types.InlineKeyboardMarkup()
    callback_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    keyboard.add(callback_yes)
    callback_no = types.InlineKeyboardButton(text="Я уже всё знаю", callback_data="no")
    keyboard.add(callback_no)
    bot.send_message(message.chat.id, "Хочешь узнать, чем я могу тебе помочь?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.data == "yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="*Здесь будет документация*. Теперь введи /reg чтобы начать")
    if call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тогда давай начнём.")


@bot.message_handler(commands=["help"])
def help_command(message):
    help_message = "Здесь будет список команд и того, что они делают \nДоступные команды:" \
                   "\n start - приветствие \n reg - ввести имя пользователя steam и т.д."
    bot.send_message(message.from_user.id, help_message)


@bot.message_handler(commands=["reg"])
def registration(message):
    bot.send_message(message.from_user.id, "Введи ссылку на аккаунт steam")
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


def get_name(message):  # получаем ссылку на профиль
    global link
    link = message.text
    if check_link_is_valid(link):
        bot.send_message(message.from_user.id, "Отлично! Что ты хочешь узнать?")
    if not check_link_is_valid(link):
        bot.send_message(message.from_user.id, "Это не является ссылкой на профиль. Нижми /reg, чтобы продолжить")


def check_link_is_valid(link: str):  # link -> bool
    components = link.split('/')
    valid = False
    for item in range(len(components)):
        if components[item] == 'steamcommunity.com':
            if components[item + 1] == 'profiles' or components[item + 1] == 'id':
                valid = True
                try:
                    id = components[item + 2]
                except IndexError:
                    break
    return valid


@bot.message_handler(commands=["link"])
def name_output(message):
    bot.send_message(message.from_user.id, "Вы ввели ссылку на профиль:")
    bot.send_message(message.from_user.id, link)



@bot.message_handler(commands=["game"])
def find_out_price(message):




if __name__ == '__main__':
    bot.polling(none_stop=True)
