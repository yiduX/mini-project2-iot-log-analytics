#!/usr/bin/env python3
"""
Reducer for Output 3: Top 10 Most Active Devices.

Input:
device_id<TAB>1

Output:
device_id count

Note:
In Hadoop Streaming, reducers only see sorted keys, but global top-10 usually needs
a second sorting step or a single reducer. For this mini-project-sized dataset, this
reducer stores device counts in memory and prints the final top 10.
"""

import sys
from collections import defaultdict


def main():
    counts = defaultdict(int)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            key, value = line.split("\t", 1)
            counts[key] += int(value)
        except ValueError:
            continue

    top10 = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    for device_id, count in top10:
        print(f"{device_id} {count}")


if __name__ == "__main__":
    main()
