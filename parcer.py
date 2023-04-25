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
    if os.path.exists(f'{vk["domain"]}'):
        print(f'Директория с именем {vk["domain"]} уже существует!')
    else:
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
        post_text = post["text"]
        # print(f"ОТправляем пост с ID {post_id}")
        try:
            post = post['attachments']
            photos_url = []
            videos_url = []

            if len(post) >= 1:
                for i in range(len(post)):
                    if post[i]['type'] == 'photo':
                        get_photo = post[i]['photo']['sizes'][3]['url']
                        photos_url.append(get_photo)
                    elif post[i]['type'] == 'video':
                        video_post_id = post[i]["video"]['id']
                        video_owner_id = post[i]["video"]['owner_id']
                        video_get_url = f"https://vk.com/video{video_owner_id}_{video_post_id}"
                        videos_url.append(video_get_url)
            else:
                pass


            print(f"{post_id} ID post have a {len(post)} attachments\nphotos:{photos_url}\nvideos:{videos_url}",
                      end='**\n\n**')
        except Exception:
            print(f"Что то пошло не так! с постом ID {post_id}!")

    # Проверка, если файла не существует значит это первый парсинг группы.
    # Отправляем все новые посты
    # Иначе осуществляем проверку и отправляем только новые посты
    #
    # if not os.path.exists(f'{vk["domain"]}/exist_posts_{vk["domain"]}.txt'):
    #     print("Файла с ID постов не существует, создаем файл")
    #     with open(f'{vk["domain"]}/exist_posts_{vk["domain"]}.txt', 'w') as file:
    #         for item in fresh_posts_id:
    #             file.write(str(item) + '\n')
    # else:
    #      print("Файл с ID постов существует, начинаем выборку свежих постов")








get_wall_post()
get_content_posts()