import requests
from config import vk
import os
import json



def get_wall_post():
    # Функция получает крайние 10-ть постов из домена и записывает их в .json
    url = f'https://api.vk.com/method/wall.get?domain={vk["domain"]}&count=20&access_token={vk["access_token"]}&v={vk["ver"]}'
    req = requests.get(url)
    src = req.json()

    # Прверяем существует ли дирректория с именем группы
    if not os.path.exists(f'{vk["domain"]}'):
        os.mkdir(vk["domain"])

    # Сохраняем данные в .json
    with open(f'{vk["domain"]}/{vk["domain"]}.json', "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)


def get_content_posts():
    # Функция собирает все посты из .json и вытягивает из них весь контент
    with open(f'{vk["domain"]}/{vk["domain"]}.json', 'r', encoding="utf-8") as file:
        src = json.load(file)
        posts = src["response"]["items"]

    for post in posts:
        post_id = post["id"]

        if not os.path.exists(f"{vk['domain']}/{post_id}"):
            os.mkdir(f"{vk['domain']}/{post_id}")

        post_text = post["text"]
        copy_text(post_id, post_text)
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



def download_photos(url, post_id, counter_jpg):
    # Функция для загрузки постов
    res = requests.get(url)
    # Создаем папку group_name/photos
    if not os.path.exists(f'{vk["domain"]}/{post_id}/photos'):
        os.mkdir(f'{vk["domain"]}/{post_id}/photos')
    with open(f'{vk["domain"]}/{post_id}/photos/{post_id}photo{counter_jpg}.jpg', "wb") as img_file:
        img_file.write(res.content)


def saved_videos(url, post_id, counter_mp4):
    # Функция для записи url video
    # Создаем папку group_name/videos
    if not os.path.exists(f"{vk['domain']}/{post_id}/video"):
        os.mkdir(f"{vk['domain']}/{post_id}/video/")
    with open(f"{vk['domain']}/{post_id}/video/{post_id}url_video{counter_mp4}.txt", "w") as url_file:
        url_file.write(url)


def copy_text(post_id, post_text):
    # Функция копирования текста из поста
    # создаем папку group_name/text
    if not os.path.exists(f"{vk['domain']}/{post_id}/text"):
        os.mkdir(f"{vk['domain']}/{post_id}/text")
    with open(f'{vk["domain"]}/{post_id}/text/{post_id}_text.txt', "w", encoding='utf-8') as text_file:
        text_file.write(post_text)

get_wall_post()
get_content_posts()