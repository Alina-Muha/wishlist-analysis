import telebot
from telebot import types
from src.steam_web_api_interactions import obtain_sales_data

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=["start"])
def start(message):
    """Приветствие пользователя. Создается переменная link, в которой хранится ссылка на аккаунт.
    Пока ссылка не введена, хранится значение -1. Создается inline клавиатура с двумя вариантами ответа."""

    global link
    link = "-1"
    bot.send_message(message.from_user.id, "Привет!")
    keyboard = types.InlineKeyboardMarkup()
    callback_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    keyboard.add(callback_yes)
    callback_no = types.InlineKeyboardButton(text="Я уже всё знаю", callback_data="no")
    keyboard.add(callback_no)
    bot.send_message(message.chat.id, "Хочешь узнать, чем я могу тебе помочь?", reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def help_command(message):
    """Команда /help. Функция выводит все доступные команды."""

    help_message = "Это список доступных команд. Введи одну из них, чтобы получить необходимую информацию. " \
                   "\n /start - начать работу с ботом. \n /reg - регистрация. " \
                   "Напиши это, чтобы ввести ссылку на аккаунт steam для дальнейшей работы. \n /link - " \
                   "эта команда нужна, чтобы узнать последнюю введенную ссылку. \n /inf - получить информацию" \
                   "о стоимости игр и скидках на них"
    bot.send_message(message.from_user.id, help_message)


@bot.message_handler(commands=["reg"])
def registration(message):
    """По запросу /reg выводит просьбу о ссылке на аккаунт steam."""
    bot.send_message(message.from_user.id, "Введи ссылку на аккаунт steam")
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


def get_name(message):
    """Получает от пользователя ссылку на аккаунт. Если ссылка некорректна, сообщает об этом пользователю."""

    global link
    link_input = message.text
    if check_link_is_valid(link_input):
        bot.send_message(message.from_user.id, "Отлично! Я запомнил")
        link = link_input
    else:
        bot.send_message(message.from_user.id, "Это не является ссылкой на профиль. Нижми /reg, чтобы продолжить")
        link = "-1"


def check_link_is_valid(link_input: str):
    """Проверяет, является ли сообщение пользователя ссылкой на профиль steam. Возвращает значение True или False."""

    components = link_input.split('/')
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


@bot.message_handler(commands=["inf"])
def information(message):
    """Получает из функции obtain_sales_data информацию о том, является ли аккаунт открытым.
    Если да, получает список игр, если нет, ссылку на настройки приватности. По команде /inf
    выдает информацию о скидках на игры или сообщает пользователю, если это невозможно сделать.
    В переменной privacy_settings хранит ссылку на настройки приватности аккаунта."""

    result = obtain_sales_data(link)
    if result[0]:
        games_output(message, result)
    else:
        global privacy_settings
        privacy_settings = result[1]
        wishlist_settings(message)


def games_output(message, result):
    """Преобразует список игр result[1] в список строк games_list с информацией об игре и список ссылок на игру
    games_link. Через функцию game_information выводит список игр со скидкой."""

    sale_list = result[1]
    games_list = []
    games_link = []
    for game in sale_list:
        games_list.append(
            f'Игра {game["Name"]} сейчас стоит {game["price"]} Скидка на нее составляет {game["discount"]}%')
        games_link.append(game["link"])
    for i in range(len(games_list)):
        game_information(message, games_link[i], games_list[i])


def game_information(message, game_link, game):
    """Выводит информацию об игре с кнопкой, при нажатии которой пользователь попадает на страницу игры."""

    button = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Страница игры", url=game_link)
    button.add(url_button)
    bot.send_message(message.chat.id, game, reply_markup=button)


def wishlist_settings(message):
    """Сообщает пользователю, почему невозножно получить информацию об играх.
    Создает inline клавиатуру с кнопкой, позволяющей перейти к настройкам приватности."""

    kb = types.InlineKeyboardMarkup()
    callback_settings = types.InlineKeyboardButton(
        text="Перейти к настройкам приватности", callback_data="settings")
    kb.add(callback_settings)
    bot.send_message(message.chat.id, "В wishlist-е нет игр со скидками, либо данные об играх скрыты", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Обрабатывает информацию с клавиатуры и возвращает сообщение в зависимости от нажатой кнопки. Запросы yes, no
     из клавиатуры keyboard, функции start и запрос settings из клавиатуры kb, функция wishlist_settings."""

    if call.data == "yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Этот бот поможет тебе получить информацию о скидках в Steam"
                                   " на игры из твоего wishlist-а или wishlist-а твоих друзей. "
                                   "Введи /help, чтобы увидеть список возможных команд.")
    if call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тогда давай начнём")

    if call.data == "settings":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Открыть настройки приватности можно в клиенте стима PROFILE -'
                                   f' Edit profile - Privacy settings - My profile: Game details - '
                                   f'поставить Public либо по ссылке в браузерее (нужно быть там залогиненым):'
                                   f' \n {privacy_settings}')


@bot.message_handler(commands=["link"])
def name_output(message):
    """По запросу /link возвращает последнюю ссылку, введенную пользователем, или сообщает, если такой ссылки нет."""

    if link == "-1":
        bot.send_message(message.from_user.id, "Ссылка на профиль еще не была введена. Чтобы ее ввести, нажми /reg")
    else:
        bot.send_message(message.from_user.id, "Последняя введенная ссылка:")
        bot.send_message(message.from_user.id, link)


if __name__ == '__main__':
    bot.polling(none_stop=True)
