# -p e32f7 -s f -b ori -m 0 -e nka -l 3 -f sha1
import argparse
import importlib

from time import gmtime, strftime, time
from typing import Callable

get_formatted_time: Callable[[], str] = lambda: "[%s]" % strftime("%Y-%m-%d %H:%M:%S", gmtime())

lib = importlib.import_module("hashlib")

parser = argparse.ArgumentParser(description='Custom hash generation tool for performance testing')
parser.add_argument("-p", "--prefix", type=str, action='store', help='Hash prefix', default="")
parser.add_argument("-s", "--suffix", type=str, action='store', help='Hash suffix', default="")
parser.add_argument("-b", "--begin",  type=str, action='store', help='Text at begin of hashing string', default="")
parser.add_argument("-m", "--middle", type=str, action='store', help='Text at middle of hashing string', default=".")
parser.add_argument("-e", "--end",    type=str, action='store', help='Text at end of hashing string', default="")
parser.add_argument("-l", "--limit",  type=lambda value: int(value) if int(value) > 0 else 10,
                    action='store', help='Stop after {limit} founded hashes', default=10)
parser.add_argument("-f", "--function", type=str, action='store', help='Hash function',
                    choices=getattr(lib, "algorithms_available"), default='sha256')
args = parser.parse_args()

function: Callable = getattr(lib, args.function)

found = 0
rounds = 0
begin_text = args.begin.encode('utf-8')
middle_text = args.middle.encode('utf-8')
end_text = args.end.encode('utf-8')

print("%s Generation started!" % get_formatted_time())

start_time = time()
while found < args.limit:
    rounds += 1
    text: bytes = begin_text + middle_text * rounds + end_text
    hash: str = function(text).hexdigest()
    if hash.endswith(args.suffix) and hash.startswith(args.prefix):
        found += 1
        print("%s Result %d, rounds %d sec %f\nHash(%s): %s\nText(%d): %s\n" %
              (get_formatted_time(), found, rounds, time() - start_time, args.function, hash, len(text), text.decode('utf-8')))
