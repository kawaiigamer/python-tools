import colorama,requests,os,time
from colorama import Fore, Back, Style
from lxml import etree
from datetime import datetime,timedelta

#---------------------------------------------------------
RSS_URL = 'https://www.fl.ru/rss/all.xml?category=5'
MAX_PRICE_LEN = 5
TITLE_OFFSET = 11
KEYWORDS = ('python', 'telegram', 'телеграм','c#')
UPDATE_TIMEOUT = 60
#---------------------------------------------------------

def fl_rss_parse(rss : str) -> list: # price,title,description,time_diff_str
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
        diff_from_now = datetime.fromtimestamp(time.time()) - ( gmt_time + timedelta(hours=3) )
        time_diff_str = str(diff_from_now)[:-10] + " "
        elements.append((price,title,description,time_diff_str))
    return elements

def display_fl_element(e : tuple) -> None:
    if len(e[0]) > MAX_PRICE_LEN:
        return
    spaces = ''.join(' ' for i in range(0, TITLE_OFFSET- (len(e[0])+len(e[3])  )))
    print(Fore.RED + e[3], end='')
    print(Fore.GREEN + e[0] + spaces, end='')
    if any(keyword in e[1].lower() for keyword in KEYWORDS):
        print(Fore.BLUE + e[1])
    else:
        print(e[1])


def mainloop() -> None:
    colorama.init(autoreset=True)
    while True:
        try:
            r = requests.get(RSS_URL)
            elements = fl_rss_parse(r.text.encode())
            os.system('cls')
            print('Updated',datetime.now().strftime("%Y-%m-%d %H:%M"))
            for e in reversed(elements):
                display_fl_element(e)
        except Exception as e:
            print('Ошибка', e)
        finally:
            time.sleep(UPDATE_TIMEOUT)


if __name__ == "__main__":
    mainloop()
