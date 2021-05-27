import os

from typing import List

MIN_FILES_COUNT = 15


def dirs(root_dit: str) -> List[str]:
    return next(os.walk(root_dit))[1]


def dir_files_count(dir_path: str) -> int:
    return len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])


def select_directory_from_list(directories: List[str]) -> str:
    for i in range(0, len(directories)):
        print("(%d) %s" % (i, directories[i]))
    while True:
        try:
            return directories[int(input('Directory to check(number)_->'))]
        except Exception as e:
            print("Wrong input: %s" % e)
            continue


def check_dirs():
    print("ckdir v1.0")
    checking_directory = select_directory_from_list(dirs('.'))
    print("Directories with file count < %d:" % MIN_FILES_COUNT)
    for inner_directory in dirs(checking_directory):
        files_count = dir_files_count("%s/%s" % (checking_directory, inner_directory))
        if files_count < MIN_FILES_COUNT:
            print("| %s -> %s" % (inner_directory, files_count))


if __name__ == "__main__":
    check_dirs()
    input("Press Enter to continue...")
