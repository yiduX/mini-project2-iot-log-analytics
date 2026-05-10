#!/usr/bin/env python3
"""
Mapper for Output 3: Top 10 Most Active Devices.

Emits:
device_id<TAB>1
"""

import csv
import sys


def is_header(row):
    return row and row[0].strip().lower() == "timestamp"


def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or is_header(row):
            continue
        try:
            device_id = row[1].strip()
        except IndexError:
            continue

        if device_id:
            print(f"{device_id}\t1")


if __name__ == "__main__":
    main()
