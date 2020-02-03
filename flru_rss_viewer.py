import colorama,requests,os,time,math,re
from colorama import Fore, Back, Style
from lxml import etree
from datetime import datetime,timedelta

#---------------------------------------------------------
RSS_URLS = (
    'https://www.fl.ru/rss/all.xml?category=5',
    #'https://www.fl.ru/rss/all.xml?category=23&subcategory=225' # Мобильные приложения - Google Android
    #'https://www.fl.ru/rss/all.xml?category=2&subcategory=9', # Разработка сайтов - Веб-программирование
           )
MAX_PRICE_LEN = 5
TITLE_OFFSET = 12
KEYWORDS = ('python', 'telegram', 'телеграм','c#')
IGNORE_KEYWORDS = ('битрикс','bitrix')
UPDATE_TIMEOUT = 60
#---------------------------------------------------------

def fl_rss_parse(rss : str) -> list: # price,title,description,time_diff
    elements = []
    root = etree.fromstring(rss)
    for item in root.xpath('//item'):
        text = item.xpath('./title')[0].text
        title = text[:text.find('(Бюджет: ')]
        if '(Бюджет: ' in text:
              price = text[text.find('(Бюджет: ') + 9:][:-10]
        else:
              price = 'П/д'
        description = item.xpath('./description')[0].text.rstrip()

        gmt_time = datetime.strptime(item.xpath('./pubDate')[0].text,"%a, %d %b %Y %H:%M:%S %Z")
        seconds_from_now = (datetime.fromtimestamp(time.time()) - ( gmt_time + timedelta(hours=3) ) ).total_seconds()
        minutes_from_now = int( math.floor(seconds_from_now / 60) )
        diff_hours = str ( int( minutes_from_now / 60 ) )
        diff_minutes =  str ( int( minutes_from_now % 60 ) )
        if len(diff_hours) == 1:
            diff_hours = '0' + diff_hours
        if len(diff_minutes) == 1:
            diff_minutes = '0' + diff_minutes
        time_diff =  diff_hours + ':' + diff_minutes + ' '

        elements.append((price,title,description,time_diff))
    return elements

def fl_display_element(e : tuple) -> bool:
    if len(e[0]) > MAX_PRICE_LEN:
        return False
    if any(keyword in e[1].lower() for keyword in IGNORE_KEYWORDS):
        return False
    spaces = ''.join(' ' for i in range(0, TITLE_OFFSET- (len(e[0])+len(e[3])  )))
    print(Fore.RED + e[3], end='')
    print(Fore.GREEN + e[0] + spaces, end='')
    if any(keyword in e[1].lower() for keyword in KEYWORDS):
        print(Fore.BLUE + e[1])
    else:
        print(e[1])
    return True


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def mainloop() -> None:
    colorama.init(autoreset=True)
    while True:
        try:
            elements = []
            for rss_url in RSS_URLS:
                r = requests.get(rss_url)
                elements += fl_rss_parse(r.text.encode())
            os.system('cls')
            elements = sorted(elements, key=lambda tup: natural_keys(tup[3]))
            filtered = 0
            for e in reversed(elements):
                if not fl_display_element(e) : filtered += 1
            print('Updated', datetime.now().strftime("%Y-%m-%d %H:%M"), 'Results', len(elements),'Filtered',filtered)
        except Exception as e:
            print('Ошибка', e)
        finally:
            time.sleep(UPDATE_TIMEOUT)


if __name__ == "__main__":
    mainloop()
