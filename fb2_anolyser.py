import os
import glob
import codecs

from typing import List

import xml.etree.ElementTree as ET

STD_LIST_CHARS = 46 * 59


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


def analyze():
    print("F2b analyser")
    checking_directory = select_directory_from_list(dirs('.'))
    f2b_files = glob.glob("%s/*.fb2" % checking_directory)
    print("Loaded %d f2b files" % len(f2b_files))
    chars_count = 0
    for f2b_file in f2b_files:
        text = ET.fromstring(codecs.open(f2b_file, 'r', encoding='utf8').read())
        for i in range(0, 2 ** 16):
            try:
                if "binary" not in text[i].tag:
                    chars_count += len(ET.tostring(text[1], encoding='utf8', method='text').decode('utf-8'))
            except Exception as e:
                print("Exception while parsing %s: %s" % (f2b_file, e))
                break
    print("Total: %f pages" % round(chars_count / STD_LIST_CHARS, 2))


if __name__ == "__main__":
    analyze()
    input("Press Enter to continue...")
