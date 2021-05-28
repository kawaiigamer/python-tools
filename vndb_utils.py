import urllib.request
import re

from typing import List, Tuple


def remote_content_http_download(url, timeout: int = 15) -> str:
    return str(urllib.request.urlopen(url, timeout=timeout).read())


def parse_char_all(url: str, count: int) -> List[List]:  # "https://vndb.org/i296?m=0;fil=tagspoil-0.trait_inc-296;p="
    links = []
    for i in range(1, count):
        text = remote_content_http_download("%s%d" % (url, i))
        links += re.findall("tc2\"><a href=\"(.+?)\" title=\".+?\">(.+?)<\/a><b", text)
    return links


def get_char_detal(chars: List[List]) -> List[Tuple]:
    new = []
    for i in range(len(chars)):
        text = remote_content_http_download("https://vndb.org%s" % chars[i][0])
        m = re.search("(\/v\d+\/chars)", text).group(1)
        try:
            link = "https://%s" % re.search("rc=\"//(.+?)\" a", text).group(1)
        except Exception:
            link = ""
        new.append((chars[i][0], chars[i][1], m, link))
    return new
