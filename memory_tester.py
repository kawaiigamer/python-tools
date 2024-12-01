import sys
import time
import random
import string
import math
from datetime import datetime
from typing import Callable, Tuple

rand_str = lambda x, n: ''.join([random.choice(x) for i in range(n)])


def clear_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def base_memory_test(str_chars: str = string.ascii_uppercase + string.digits, str_len: int = 10) -> Tuple[str, str]:
    test_str = rand_str(str_chars, str_len)
    return test_str, test_str


def base_math_test(numbers_count: int = 2, lower: int = 1000000, upper: int = 10000000) -> Tuple[str, str]:
    numbers = [random.randint(lower, upper) for i in range(numbers_count)]
    return " * ".join(map(str, numbers)) + " = ?", str(math.prod(numbers))


def mainloop(func: Callable[[], Tuple[str, str]], sleep_time_sec: float):
    try_no = 1
    successful_tries = 0
    time_started = time_started_current = datetime.now()

    while True:
        now = datetime.now()
        time_overall = (now - time_started).total_seconds() - ((try_no - 1) * sleep_time_sec)
        last_time = (now - time_started_current).total_seconds() - sleep_time_sec if try_no > 1 else 0
        print(f"------\nTry number: {try_no}, Successful Tries: {successful_tries}, Percent:",
              "0.0%" if try_no == 1 else f"{(successful_tries / (try_no - 1)):.1%}",
              f"Time overall: {time_overall:.1f}s", f"Last time: {last_time:.1f}s")
        time_started_current = datetime.now()
        test_representation, test_result = func()
        print(test_representation)
        time.sleep(sleep_time_sec)
        clear_last_line()
        inputted_str = input("->")
        if test_result.upper() == inputted_str.upper():
            print("Succeed")
            successful_tries += 1
        else:
            print(f"Failed, Correct result: {test_result}")
        try_no += 1


if __name__ == "__main__":
    mainloop(lambda: base_memory_test(str_len=60), 5)  # mainloop(lambda: base_math_test(4), 5)
