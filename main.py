import telebot
from telebot import types
from config import token, adminuser, chunnelid
from parcer import *
import time

# TODO определиться с БД и ее использованием для взаоимодействия с пользователями


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'site', 'ivent', 'info', 'admin'])
def main(message):
    # Обработчик команд
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.username}')
        bot.send_message(message.chat.id, 'Что ты хочешь узнать?')
    elif message.text == '/site':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти на сайт доставки.',
                                              url='https://www.delivery-club.ru/r/nalivocnaa_rodina'))
        bot.send_message(message.chat.id, 'Передаю ссылку на сайт, для заказа еды!', reply_markup=markup)

    elif message.text == '/ivent':
        bot.send_message(message.chat.id, 'Сейчас расскажу про акции, выбери день'
                                          'в который хочешь к нам заглянуть?')

    # Отправка .json обьекта с информацией о пользователе
    elif message.text == '/info':
        bot.send_message(message.chat.id, message)

    # Вызов админ панели
    elif message.text == '/admin':
        if str(message.from_user.id) in adminuser:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Загрузить посты из группы вк", callback_data='download'))
            markup.add(types.InlineKeyboardButton("Сверить наличие новых постов", callback_data='parse'))
            markup.add(types.InlineKeyboardButton("Редактировать мероприятия", callback_data='edit'))
            bot.send_message(message.chat.id, 'Приветсвую Мастер!\nЧто вы хотите сделать?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'В доступе отказано!')


@bot.message_handler()
def interaction(message):
    # Обработчик текстовых данных присланных пользователем или админом
    if message.text == 'push' and str(message.from_user.id) in adminuser:
        bot.reply_to(message, f'обрабатываю ваш запрос')
        print(message)
        # TODO использовать не перессылку сообщения, а данные сообщения из message.json
        bot.forward_message(chat_id=chunnelid, from_chat_id=message.chat.id, message_id=message.reply_to_message.id)


@bot.callback_query_handler(func=lambda callback: True)
def callback_admin(callback):
    # Обработчик админ запросов
    if callback.data == 'download':
        bot.send_message(callback.message.chat.id, text=get_wall_post())
        get_content_posts()
    elif callback.data == 'parse':
        bot.send_message(callback.message.chat.id, text=check_new_posts())
    # в данный момент кнопка edit отправляет каскад сообщений содержащих постов из вк в телеграм
    elif callback.data == 'edit':
        # bot.send_message(chat_id=callback.message.chat.id, text=callback)
        files = os.listdir(f"{vk['domain']}")
        if len(files) > 2:
            for name in files:
                if name != 'posts_id.txt' and name != f'{vk["domain"]}.json':
                    if len(os.listdir(f"{vk['domain']}/{name}")) > 1:
                        items = os.listdir(f"{vk['domain']}/{name}/photos/")
                        text = open(f"{vk['domain']}/{name}/text/{name}text.txt", 'r', encoding='utf-8')
                        if len(items) > 1:
                            photos = []
                            counter = 0
                            for item in items:
                                photo = open(f"{vk['domain']}/{name}/photos/{item}", 'rb')
                                if counter != 0:
                                    photos.append(telebot.types.InputMedia(type='photo', media=photo))
                                else:
                                    photos.append(telebot.types.InputMedia(type='photo', media=photo,
                                                                           caption=text.read()))
                                counter += 1
                            bot.send_media_group(chat_id=callback.message.chat.id, media=photos)
                        else:
                            photo = open(f"{vk['domain']}/{name}/photos/{name}photo0.jpg", 'rb')
                            bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption=text.read())
                    else:
                        text = open(f"{vk['domain']}/{name}/text/{name}text.txt", 'r', encoding='utf-8')
                        bot.send_message(chat_id=callback.message.chat.id, text=text.read())
                time.sleep(5)
        else:
            bot.send_message(chat_id=callback.message.chat.id, text='Нет доступных постов для публикации,'
                                                                    ' попробуйте сверить наличие новых постов.')


# Бесконечный цикл работы
if __name__ == '__main__':
    bot.polling(none_stop=True)


def send_posts(id):
    # Пробная запись функции отправки каскада постов
    files = os.listdir(f"{vk['domain']}")

    for name in files:
        if name != 'posts_id.txt' and name != f'{vk["domain"]}.json':
            if len(os.listdir(f"{vk['domain']}/{name}")) > 1:
                items = os.listdir(f"{vk['domain']}/{name}/photos/")
                text = open(f"{vk['domain']}/{name}/text/{name}text.txt", 'r', encoding='utf-8')
                if len(items) > 1:
                    photos = []
                    counter = 0
                    for item in items:
                        photo = open(f"{vk['domain']}/{name}/photos/{item}", 'rb')
                        if counter == 0:
                            photos.append(telebot.types.InputMedia(type='photo', media=photo, caption=text.read()))
                        else:
                            photos.append(telebot.types.InputMedia(type='photo', media=photo))
                        counter += 1

                    bot.send_media_group(id, media=photos)
                else:
                    photo = open(f"{vk['domain']}/{name}/photos/{name}photo0.jpg", 'rb')
                    bot.send_photo(id, photo=photo, caption=text.read())
            else:
                text = open(f"{vk['domain']}/{name}/text/{name}text.txt", 'r', encoding='utf-8')
                bot.send_message(id, text=text.read())
        time.sleep(5)
