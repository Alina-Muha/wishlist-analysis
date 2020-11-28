import telebot
from telebot import types

bot = telebot.TeleBot('1486307406:AAFYJJHnIChyLvxpS_a9O0y7xumya1__-L8')


@bot.message_handler(content_types=["text"])
def any_msg(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет!")
        keyboard = types.InlineKeyboardMarkup()
        callback_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
        keyboard.add(callback_yes)
        callback_no = types.InlineKeyboardButton(text="Я уже всё знаю", callback_data="no")
        keyboard.add(callback_no)
        bot.send_message(message.chat.id, "Хочешь узнать, чем я могу тебе помочь?", reply_markup=keyboard)
    elif message.text == "/help" or message.text == "/start":
        bot.send_message(message.from_user.id, "Напиши мне привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши мне привет, чтобы начать.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.data == "yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    if call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Бдыщь")


if __name__ == '__main__':
    bot.polling(none_stop=True)
