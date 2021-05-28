import os
import sys
import urllib.request
import re
import socket

from concurrent.futures import ThreadPoolExecutor
from time import gmtime, strftime, time
from typing import List, Tuple, Union


def get_size(start_path: str) -> int:
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def get_formatted_time() -> str:
    return "[%s]" % strftime("%Y-%m-%d %H:%M:%S", gmtime())


def atoi(text: str) -> Union[int, str]:
    return int(text) if text.isdigit() else text


def natural_keys(text: str) -> List[Union[int, str]]:
    return [atoi(key) for key in re.split('(\d+)', text)]


def remote_content_http_download(url, timeout: int = 15) -> bytes:
    return urllib.request.urlopen(url, timeout=timeout).read()


def console_integer_input(description, _min: int, _max: int, default: int) -> int:
    while True:
        try:
            console_input: str = input("%s ->(%d-%d) " % (description, _min, _max))
            if not console_input:
                print("Using default(%s) -> %d" % (description, default))
                return default
            console_input: int = int(console_input)
            if _min > console_input or console_input > _max:
                raise Exception("Entered value is out of range")
            return console_input
        except Exception as e:
            print("Wrong input: %s" % e)


def get_integer_argument(argv_index, description, _min: int, _max: int, default: int) -> int:
    if len(sys.argv) > argv_index:
        try:
            value = int(sys.argv[argv_index])
            if _min > value > _max:
                raise Exception("Argv value is out of range(%d-%d)" % (_min, _max))
            print("%s -> %d" % (description, value))
            return value
        except Exception as e:
            print("Wrong argv value(%s): %s, using default(%s) -> %d" % (description, e, description, default))
            return default
    return console_integer_input(description, _min, _max, default)


def remove_url_arguments(url: str) -> str:
    args_position = url.find("?")
    return url[:args_position] if args_position != -1 else url


def concurrent_manga_chapter_download(task: str, page_download_retries_count: int,
                                      img_download_retries_count: int, downloaded_size_list: List):
    _ = task.split("/")  # task - /asura/vol1/1
    chapter_directory_name = "%s/%s_%s" % (manga_name, _[len(_) - 2], _[len(_) - 1])
    os.makedirs(chapter_directory_name, exist_ok=True)
    print("%s Creating new directory : %s" % (get_formatted_time(), chapter_directory_name))

    final_url = "%s%s?mature=1" % (domain, task)
    while True:  # TODO: retrys
        try:
            raw = str(remote_content_http_download(final_url))
        except Exception as e:
            print("%s Exception in task %s while downloading %s: %s" %
                  (get_formatted_time(), task, final_url, e))
            continue
        break

    chapter_img_urls = re.findall("\'(.+?)'..(.+?)'.\"(.+?)\"", raw[raw.index('.init'):][:5500])
    for i in range(len(chapter_img_urls)):
        url = chapter_img_urls[i][1] + chapter_img_urls[i][0] + chapter_img_urls[i][2]
        while True:
            try:
                image_url = url[1:].replace("\\", "")
                image_save_path = remove_url_arguments(chapter_directory_name + "\\" + url.split('/')[-1])
                urllib.request.urlretrieve(image_url, image_save_path)
            except Exception as e:
                print(get_formatted_time(), _, str(e), url[1:].replace("\\", ""))
                continue
            break
    downloaded_size_list.append(get_size(chapter_directory_name))


# -- Preset
page_download_retries_count = 3
img_download_retries_count = 3
downloaded_size = []
socket.setdefaulttimeout(30)

# -- Getting Url
base_url = sys.argv[1] if len(sys.argv) > 1 else input("URL ->(ex. https://readmanga.live/asura) ")
domain = base_url[:base_url.rindex('/')]  # https://readmanga.live
manga_name = remove_url_arguments(base_url[base_url.rindex('/'):])  # /asura

# -- Getting chapters catalog
raw_catalog = str(remote_content_http_download(base_url))
chapters_list = list(set(re.compile('<a href=\"(%s/vol\d+/\d+)' % manga_name, re.M).findall(raw_catalog)))
chapters_list.sort(key=natural_keys)
manga_name = manga_name[1:]  # Remove slash at start /asura -> asura
print("found: %d chapters" % len(chapters_list))

# -- Getting Input
from_chapter = get_integer_argument(2, "Start from", 0, len(chapters_list), default=0)
to_chapter = get_integer_argument(3, "Stop at", from_chapter, len(chapters_list), default=len(chapters_list))
threads = get_integer_argument(4, "Threads", 10, 100, default=10)

# -- Making dir
os.makedirs(manga_name, exist_ok=True)
print("%s Creating new directory : %s" % (get_formatted_time(), manga_name))

# -- Downloading
start_time = time()
with ThreadPoolExecutor(max_workers=threads) as executor:
    i = from_chapter
    while i < to_chapter:
        executor.submit(lambda: concurrent_manga_chapter_download(chapters_list[i], page_download_retries_count,
                                                                  img_download_retries_count, downloaded_size))
        i += 1
    executor.shutdown()

# -- Finalizing
download_size_mb = round(sum(downloaded_size) / 1048576, 3)
download_time = int(time() - start_time)
print("%f MB downloaded from %d seconds, %f MB per second" %
      (download_size_mb, download_time, round(download_size_mb / download_time, 3)))
if len(sys.argv) != 5:  # If user makes input
    input("press Enter to continue...")
