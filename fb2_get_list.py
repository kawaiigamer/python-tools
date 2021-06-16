import os
import glob
import codecs

from typing import List


def dirs(root_dit: str) -> List[str]:
    return next(os.walk(root_dit))[1]


def select_directory_from_list(directories: List[str]) -> str:
    for i in range(0, len(directories)):
        print("(%d) %s" % (i, directories[i]))
    while True:
        try:
            return directories[int(input('Directory to check(number)_->'))]
        except Exception as e:
            print("Wrong input: %s" % e)
            continue


def text_between(_str: str, begin: str, end: str) -> str:
    start = _str.find(begin)
    stop = _str.find(end)
    if start != -1 and stop != -1:
        return _str[start+len(begin):stop]
    else:
        return ""


def f2b_print_data_list():
    checking_directory = select_directory_from_list(dirs('.'))
    f2b_files = glob.glob("%s/*.fb2" % checking_directory)
    counter = 0
    for f2b_file in f2b_files:
        try:
            text = codecs.open(f2b_file, 'r', encoding='utf8').read()
            counter += 1
            print("%d. %s - %s %s %s" %
                  (counter,
                   text_between(text, "<book-title>", "</book-title>"),
                   text_between(text, "<first-name>", "</first-name>"),
                   text_between(text, "<middle-name>", "</middle-name>"),
                   text_between(text, "<last-name>", "</last-name>")
                   ))
        except Exception as e:
            print("Exception while parsing %s: %s" % (f2b_file, e))


if __name__ == "__main__":
    f2b_print_data_list()
