#!/usr/bin/env python3
"""
Mapper for Output 1: Event Count by Sensor Type.

Input CSV columns:
timestamp,device_id,building,floor,room,sensor_type,event_type,value,status,battery_level

Emits:
sensor_type<TAB>1
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
            sensor_type = row[5].strip()
        except IndexError:
            continue

        if sensor_type:
            print(f"{sensor_type}\t1")


if __name__ == "__main__":
    main()
