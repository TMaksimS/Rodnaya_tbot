import requests
from config import vk
import os
import json



def get_wall_post():
    # Функция получает крайние 10-ть постов из домена и записывает их в .json
    url = f'https://api.vk.com/method/wall.get?domain={vk["domain"]}&count=10&access_token={vk["access_token"]}&v={vk["ver"]}'

    req = requests.get(url)
    src = req.json()

    # Прверяем существует ли дирректория с именем группы
    if not os.path.exists(f'{vk["domain"]}'):
        os.mkdir(vk["domain"])

    # Сохраняем данные в .json
    with open(f'{vk["domain"]}/{vk["domain"]}.json', "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
    message = 'Крайние 10-ть постов были загружены'
    return message


def get_content_posts(last_post_id=None):
    # Функция собирает все посты из .json и вытягивает из них весь контент
    with open(f'{vk["domain"]}/{vk["domain"]}.json', 'r', encoding="utf-8") as file:
        src = json.load(file)
        posts = src["response"]["items"]
        # Собираем все посты в список, для записи их id в .txt
        fresh_posts_id = ''
    # Цикл прохода по всем постам полученым из .json
    for post in posts:
        post_id = post["id"]
        fresh_posts_id += f' {post_id}'
        # Проверка на наличие крайнего поста, если он задан, то цикл прервется и сохранит только свежие посты
        if last_post_id == str(post_id):
            break
        # Создаем деррикторию группы
        if not os.path.exists(f"{vk['domain']}"):
            os.mkdir(f"{vk['domain']}")
        # Создаем дирректорию для каждого поста
        if not os.path.exists(f"{vk['domain']}/{post_id}"):
            os.mkdir(f"{vk['domain']}/{post_id}")
        # Сохраняем текст публикации
        post_text = post["text"]
        copy_text(post_id, post_text)
        # Если пост содержит вложение и не состоит только из текста, проходим по всем вложениям и проверяем их тип
        post = post['attachments']
        counter_jpg = 0
        counter_mp4 = 0
        if len(post) >= 1:
            for i in range(len(post)):
                if post[i]['type'] == 'photo':
                    get_photo = post[i]['photo']['sizes'][3]['url']
                    download_photos(get_photo, post_id, counter_jpg)
                    counter_jpg += 1
                elif post[i]['type'] == 'video':
                    video_duration = post[i]["video"]['duration']
                    if video_duration <= 300:
                        video_post_id = post[i]["video"]['id']
                        video_owner_id = post[i]["video"]['owner_id']
                        video_get_url = f"https://vk.com/video{video_owner_id}_{video_post_id}"
                        saved_videos(video_get_url, post_id, counter_mp4)
                        counter_mp4 += 1
    # В дирректории группы создаем документ, в котором мы записываем ID всех полученных постов из группы
    with open(f"{vk['domain']}/posts_id.txt", 'w') as file:
        file.write(f"{fresh_posts_id} ")
    message = 'Контент из постов был получен'
    return message


def download_photos(url, post_id, counter_jpg):
    # Функция для загрузки фотографий из постов
    res = requests.get(url)
    # Создаем папку group_name/id/photos
    if not os.path.exists(f'{vk["domain"]}/{post_id}/photos'):
        os.mkdir(f'{vk["domain"]}/{post_id}/photos')
    with open(f'{vk["domain"]}/{post_id}/photos/{post_id}photo{counter_jpg}.jpg', "wb") as img_file:
        img_file.write(res.content)


def saved_videos(url, post_id, counter_mp4):
    # Функция для записи url video, проблема с загрузкой видео, как вариант перезаписать token vk api
    # Пока что реализуем только сохрание ссылки на видео
    # Создаем папку group_name/id/videos
    if not os.path.exists(f"{vk['domain']}/{post_id}/video"):
        os.mkdir(f"{vk['domain']}/{post_id}/video/")
    with open(f"{vk['domain']}/{post_id}/video/{post_id}url_video{counter_mp4}.txt", "w") as url_file:
        url_file.write(url)


def copy_text(post_id, post_text):
    # Функция записи текста из поста
    # создаем папку group_name/id/text
    if not os.path.exists(f"{vk['domain']}/{post_id}/text"):
        os.mkdir(f"{vk['domain']}/{post_id}/text")
    with open(f'{vk["domain"]}/{post_id}/text/{post_id}text.txt', "w", encoding='utf-8') as text_file:
        text_file.write(post_text)


def check_new_posts():
    # Функция проверки наличия новых постов
    url = f'https://api.vk.com/method/wall.get?domain={vk["domain"]}&count=10&access_token={vk["access_token"]}&v={vk["ver"]}'
    req = requests.get(url)
    src = req.json()
    new_post_id = src['response']['items'][0]['id']
    # просматриваем крайние загруженные посты по ID
    with open(f"{vk['domain']}/posts_id.txt", "r", encoding="utf-8") as old_posts:
        content = old_posts.read()
        old_posts_id = content.strip().split(' ')
    # Проверяем ID новых постов с крайним старым ID
    if new_post_id != int(old_posts_id[0]):
        with open(f'{vk["domain"]}/{vk["domain"]}.json', "w", encoding="utf-8") as file:
            json.dump(src, file, indent=4, ensure_ascii=False)
        get_content_posts(last_post_id=old_posts_id[0])
        message = 'Новые посты найдены и были загружены, готовим их к публикации'
        return message
    else:
        message = 'Не найдено новых постов'
        return message
