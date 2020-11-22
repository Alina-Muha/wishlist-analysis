
import telebot
from telebot import types

bot = telebot.TeleBot('1486307406:AAFYJJHnIChyLvxpS_a9O0y7xumya1__-L8')
@bot.message_handler(content_types=['text'])

def begining (message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Напиши мне привет, чтобы начать")


def get_text_messages(message):
    bot.send_message(message.from_user.id, "лол ничего не работает")
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Я уже всё умею', callback_data='no')
    keyboard.add(key_no)
    if message.text == 'Привет':
        question = "Привет! Xочешь узнать, чем я могу тебе помочь?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши мне привет,чтобы начать.")

bot.polling(none_stop=True, interval=0)


@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call, message):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(message.from_user.id, "Документация. Теперь введи /reg чтобы начать")
    elif call.data == "no":
        bot.send_message(message.from_user.id, "Тогда давай начнем. Введи /reg")

def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введи имя пользователя steam")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем имя пользователя
    global name
    name = message.text