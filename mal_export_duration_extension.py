"""
This script adds a missing "duration" field for every anime in the list retrieved via official myanimelist export api(https://myanimelist.net/panel.php?go=export)
"""
import sys
from typing import Optional

import xml.etree.ElementTree as ET
from mal import Anime


def get_duration(amime_id: int) -> Optional[str]:
    return Anime(amime_id).duration


def modify(path: str):
    tree = ET.parse(path)
    root = tree.getroot()
    counter = 0
    global_len = len(root)
    for element in root:
        if element.tag == "anime":
            counter += 1
            try:
                duration: str = get_duration(int(element.find("series_animedb_id").text))
            except Exception as e:
                print("Exception while updating %d/%d - %s -> %s" % (counter, global_len, element.find("series_title").text, e))
                continue
            duration_element = ET.Element("duration")
            duration_element.text = duration
            duration_element.tail = "\n                    "
            element.insert(1, duration_element)
            print("Updating %d/%d - %s -> %s" % (counter, global_len, element.find("series_title").text, duration))
    tree.write(path, encoding="utf-8", xml_declaration=True)
    print("Overwrite is successful: %s" % path)

    
if __name__ == "__main__":
    modify(sys.argv[1])
    print("Work is done!")
