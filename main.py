import telebot
from telebot import types
from api import token

# TODO убрать токен в другой файл
# TODO добавить кнопки на акции и их описание, по дням недели
# TODO определиться с БД и ее использованием для акций 
# TODO изучить вопрос публикации постов в группе через бота
# TODO парсить профиль в инстаграмме и на его основе создавать посты в группу

bot = telebot.TeleBot(token)

"""Обработчик команд"""
@bot.message_handler(commands=['start', 'site', 'ivent'])
def main(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.username}')
        bot.send_message(message.chat.id, 'Что ты хочешь узнать?')
    elif message.text == '/site':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти на сайт доставки.',
                                              url='https://www.delivery-club.ru/r/nalivocnaa_rodina'))
        bot.send_message(message.chat.id, 'Передаю ссылку на сайт, для заказа еды!', reply_markup=markup)

    elif message.text == '/ivent':
        markup = types.InlineKeyboardMarkup()
        """markup.add(types.InlineKeyboardButton())"""
        bot.send_message(message.chat.id, 'Сейчас расскажу про акции, выбери день'
                                          'в который хочешь к нам заглянуть?')


"""Бесконечный цикл работы"""
bot.polling(none_stop=True)
