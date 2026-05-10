#!/usr/bin/env python3
"""
Mapper for Output 2: Warning/Error Count by Building.

Counts records where status is WARNING or ERROR.

Emits:
building<TAB>1
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
            building = row[2].strip()
            status = row[8].strip().upper()
        except IndexError:
            continue

        if building and status in {"WARNING", "ERROR"}:
            print(f"{building}\t1")


if __name__ == "__main__":
    main()
