import requests
from config import vk
import os
import json



def get_wall_post():
    url = f'https://api.vk.com/method/wall.get?domain={vk["domain"]}&count=10&access_token={vk["access_token"]}&v={vk["ver"]}'
    req = requests.get(url)
    src = req.json()

    # Прверяем существует ли дирректория с именем группы
    if os.path.exists(f'{vk["domain"]}'):
        print(f'Директория с именем {vk["domain"]} уже существует!')
    else:
        os.mkdir(vk["domain"])

    # Сохраняем данные в .json
    with open(f'{vk["domain"]}/{vk["domain"]}.json', "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # Собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for post in posts:
        post_id = post['id']
        fresh_posts_id.append(post_id)

    # Проверка, если файла не существует значит это первый парсинг группы.
    # Отправляем все новые посты
    # Иначе осуществляем проверку и отправляем только новые посты

    if not os.path.exists(f'{vk["domain"]}/exist_posts_{vk["domain"]}.txt'):
        print("Файла с ID постов не существует, создаем файл")
        with open(f'{vk["domain"]}/exist_posts_{vk["domain"]}.txt', 'w') as file:
            for item in fresh_posts_id:
                file.write(str(item) + '\n')
    else:
         print("Файл с ID постов существует, начинаем выборку свежих постов")

        # Извлекаем данные из постов
    for post in posts:
        post_id = post["id"]
        post_text = post["text"]
        print(f"ОТправляем пост с ID {post_id}")
        try:
            if 'attachments' in post:
                post = post['attachments']

                if len(post) >= 1 and post[0]['type'] == 'photo':
                    photos_url = []
                    for i in range(len(post)):
                        get_photo = post[i]['photo']['sizes'][3]['url']
                        photos_url.append(get_photo)
                    print(f"{post_id} ID post have a {len(post)} photos\n{photos_url}\n Text post: {post_text}", end='****\n\n\n\n****')

        except Exception:
                print(f"Что то пошло не так! с постом ID {post_id}!")






get_wall_post()