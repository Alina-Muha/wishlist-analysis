import telebot
from telebot import types

bot = telebot.TeleBot('1486307406:AAFYJJHnIChyLvxpS_a9O0y7xumya1__-L8')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет!")
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data=1)  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Я уже всё умею', callback_data=2)
        keyboard.add(key_no)
        question = "Xочешь узнать, чем я могу тебе помочь?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.text == "/help" or message.text == "/start":
        bot.send_message(message.from_user.id, "Напиши мне привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши мне привет, чтобы начать.")


bot.polling(none_stop=True, interval=0)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    answer = ""
    if call.data == 1:  # call.data это callback_data, которую мы указали при объявлении кнопки
        answer = 'Здесь будет документация. Теперь введи /reg чтобы начать'
        # bot.send_message(message.from_user.id, )
    elif call.data == 2:
        answer = 'Тогда давай начнем. Введи /reg'
    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введи имя пользователя steam")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):  # получаем имя пользователя
    global name
    name = message.text
