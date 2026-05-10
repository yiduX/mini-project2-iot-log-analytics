#!/usr/bin/env python3
"""
Reducer for Output 2: Warning/Error Count by Building.

Input:
building<TAB>1

Output:
building count
"""

import sys


def emit(key, count):
    if key is not None:
        print(f"{key} {count}")


def main():
    current_key = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            key, value = line.split("\t", 1)
            value = int(value)
        except ValueError:
            continue

        if current_key is None:
            current_key = key
            current_count = value
        elif key == current_key:
            current_count += value
        else:
            emit(current_key, current_count)
            current_key = key
            current_count = value

    emit(current_key, current_count)


if __name__ == "__main__":
    main()
