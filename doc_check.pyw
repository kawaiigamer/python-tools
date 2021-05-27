import requests
import json
import ctypes
import time

tasks = [
    # speciality_id, clinic_id, name '' - for any name, description
    (40, 279, '', 'desc 1'),
    (2122, 314, 'Name', 'desc 2'),
]

request_headers = {
    'Host': 'gorzdrav.spb.ru',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://gorzdrav.spb.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://gorzdrav.spb.ru/signup/free/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6'
}


def doc_check():
    for task in tasks:
        r = requests.post("https://gorzdrav.spb.ru/api/doctor_list/",
                          data="speciality_form-speciality_id=%s&speciality_form-clinic_id=%s&speciality_form-patient_id=&speciality_form-history_id=" %
                               (task[0], task[1]),
                          headers=request_headers)
        resp = json.loads(r.text)
        for doc in resp.get('response', []):
            if doc['CountFreeTicket'] is not 0 and task[2] in doc['Name']:
                ctypes.windll.user32.MessageBoxW(0, "New ticket available!\n" + task[3] + "  match: " + task[2],
                                                 time.ctime(), 4096)
                if task[2] is '':
                    break


while True:
    doc_check()
    time.sleep(65)
