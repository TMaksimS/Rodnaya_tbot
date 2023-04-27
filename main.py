import telebot
from telebot import types
from config import token, adminuser, chunnelid
from parcer import *

# TODO определиться с БД и ее использованием для акций
# TODO изучить вопрос публикации постов в группе через бота
# TODO парсить профиль в инстаграмме и на его основе создавать посты в группу

bot = telebot.TeleBot(token)

"""Обработчик команд"""
@bot.message_handler(commands=['start', 'site', 'ivent', 'info', 'admin'])
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
    elif message.text == '/info':
        bot.send_message(message.chat.id, message)

    elif message.text == '/admin':
        if str(message.from_user.id) in adminuser:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Загрузить посты из группы вк", callback_data='download'))
            markup.add(types.InlineKeyboardButton("Сверить наличие новых постов", callback_data='parse'))
            markup.add(types.InlineKeyboardButton("Подготовить новые посты в группу", callback_data='sendler'))
            markup.add(types.InlineKeyboardButton("Редактировать мероприятия", callback_data='edit'))
            bot.send_message(message.chat.id, 'Приветсвую Мастер!\nЧто вы хотите сделать?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'В доступе отказано!')

# Обработчик админ запросов
@bot.callback_query_handler(func=lambda callback: True)
def callback_admin(callback):
    if callback.data == 'sendler':
        bot.send_message(chat_id=chunnelid, text='Привет')
    # elif callback.data == 'download':
    #     get_wall_post()
    #     get_content_posts()
    elif callback.data == 'edit':
        bot.send_message(chat_id=chunnelid, text='Пока что нечего редактировать')

# Бесконечный цикл работы
if __name__ == '__main__':
    bot.polling(none_stop=True)
