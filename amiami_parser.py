import time
import sys
import urllib.request
import socket
import re

from typing import List


class EntitiesNotFound(Exception):
    pass


timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 10
path = str(sys.argv[2]) if len(sys.argv) > 2 else "http://www.amiami.jp/top/page/c/bishoujo.html"
values = []
print("[%s] timeout -> %d sec, path -> %s" % (time.strftime("%Y/%m/%d %H:%M:%S"), timeout, path))
print("---------------------------")
try:
    raw_html = str(urllib.request.urlopen(path, timeout=timeout).read())
    product_type = re.findall(re.compile("</font>(\d+,\d+)"), raw_html)
    values: List[int] = [int(x.replace(",", "")) for x in product_type]
    total_price = sum(values)
    products_count = len(values)
    if not products_count:
        raise EntitiesNotFound("Nothing found")
    print("All: %d 円" % total_price)
    print("For: %d matches" % products_count)
    print("Srd: %f 円" % (total_price / products_count))
    print("Min: %d 円" % min(values))
    print("Max: %d 円" % max(values))
    print("List:\n%s" % "\n".join(str(x) for x in sorted(values)))
except (urllib.request.URLError, socket.timeout, EntitiesNotFound) as e:
    print("Parsing error: %s" % e)
