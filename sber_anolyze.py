import re

from typing import List

PLUS_REGEX = "SBOL.+?([\d+]+).00CR"
MINUS_REGEX = "QIWI WALLET.+?([\d+]+).[\d+]+$"


def sber_get_transactions_amount(file_path: str, regex: str, start_at_line: int = 0, stop_at_line: int = 0,
                                 min_value: int = 500, max_value: int = 2**32) -> List[int]:
    numbers = []
    data = [line.strip() for line in open(file_path, 'r')]
    if stop_at_line == 0:
        stop_at_line = len(data)
    for line in data[start_at_line:stop_at_line]:
        r = re.search(regex, line)
        if r:
            numbers.append(int(r.group(1)))
    return [x for x in numbers if min_value < x < max_value]


def print_transactions_info(transactions: List[int]):
    print(transactions)
    print("SUM: %d" % sum(transactions))


if __name__ == "__main__":
    filename = "15081_Jan19.txt"
    print("Ingoing transactions")
    print_transactions_info(sber_get_transactions_amount(filename, PLUS_REGEX))
    print("QIWI Outgoing transactions")
    print_transactions_info(sber_get_transactions_amount(filename, MINUS_REGEX))
