import vk_api
import datetime
import requests
import sqlite3

from typing import List


def get_vk_image(url) -> bytes:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass


def photos_in_attachment(src: List[str]) -> List[str]:
    photos = []
    for i in src:
        if 'photo' in i:
            photos.append(i.replace('photo_', ''))
    return photos


def main(login: str, password: str, group_id: int):
    vk = vk_api.VkApi(login, password)
    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk)
    wall = tools.get_all('wall.get', 100, {'owner_id': group_id})
    print('Posts count:', wall['count'])
    con = sqlite3.connect('data1.sqllite')
    cur = con.cursor()
    i = 0
    for post in reversed(wall['items']):
        i = i + 1
        print('>', i)
        post_id = post['id']
        poster_id = post['from_id']
        _ = vk.method('users.get', {'user_ids': post['from_id'], 'fields': 'photo_50'})
        try:
            date_name = datetime.datetime.utcfromtimestamp(int(post['date'])).strftime('%Y-%m-%d %H:%M:%S') + "  " + \
                        _[0]['first_name'] + " " + _[0]['last_name']
        except Exception:
            date_name = datetime.datetime.utcfromtimestamp(int(post['date'])).strftime('%Y-%m-%d %H:%M:%S') + "  Admin"
        date = post['date']
        likes = post['likes']['count']
        text = post['text'].encode("utf-8", errors='ignore')
        try:
            poster_photo = get_vk_image(_[0]['photo_50'])
        except Exception:
            poster_photo = None
        ins = []
        if 'attachments' in post:
            for attachment in post['attachments']:
                if attachment['type'] == 'photo':
                    _3 = sorted(photos_in_attachment(attachment['photo'].keys()), key=int)
                    ins.append(get_vk_image(attachment['photo']["photo_" + _3[len(_3) - 1]]))

        table = [post_id, poster_id, date_name, date, likes, text, poster_photo]

        for w in range(10):
            if 0 <= w < len(ins):
                table.append(ins[w])
            else:
                table.append(None)

        cur.execute('''INSERT INTO selfharm(post_id, poster_id, date_name, date, likes, text, poster_photo, insert_1, insert_2, insert_3, insert_4, insert_5, insert_6, insert_7, insert_8, insert_9, insert_10)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', table)
        con.commit()


if __name__ == "__main__":
    main('', '', -29177169)

