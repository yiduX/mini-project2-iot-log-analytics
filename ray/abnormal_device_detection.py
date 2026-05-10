#!/usr/bin/env python3
"""
Ray extension: Abnormal Device Detection.

A device is abnormal if it satisfies at least one condition:
1. battery_level < 20
2. status = ERROR in at least 3 records
3. temperature value > 32 in at least 3 records

Output CSV:
device_id,building,reason

Usage:
python3 ray/abnormal_device_detection.py data/iot_logs.csv outputs/abnormal_devices.csv
"""

import csv
import math
import os
import sys
from collections import defaultdict

import ray


def safe_float(value):
    try:
        if value is None or value == "":
            return None
        return float(value)
    except ValueError:
        return None


def safe_int(value):
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except ValueError:
        return None


def combine_device_stats(left, right):
    """
    Merge right-side per-device stats into left-side per-device stats.
    """
    for device_id, r in right.items():
        l = left[device_id]
        if not l["building"] and r["building"]:
            l["building"] = r["building"]

        l["low_battery"] = l["low_battery"] or r["low_battery"]
        l["error_count"] += r["error_count"]
        l["high_temp_count"] += r["high_temp_count"]

    return left


@ray.remote
def process_rows(rows):
    """
    Process a chunk of CSV rows in parallel.

    Returns a dict:
    {
      device_id: {
        "building": str,
        "low_battery": bool,
        "error_count": int,
        "high_temp_count": int
      }
    }
    """
    stats = defaultdict(lambda: {
        "building": "",
        "low_battery": False,
        "error_count": 0,
        "high_temp_count": 0,
    })

    for row in rows:
        if not row or row[0].strip().lower() == "timestamp":
            continue

        try:
            device_id = row[1].strip()
            building = row[2].strip()
            sensor_type = row[5].strip().lower()
            value = row[7].strip()
            status = row[8].strip().upper()
            battery_level = row[9].strip()
        except IndexError:
            continue

        if not device_id:
            continue

        device_stats = stats[device_id]
        if building and not device_stats["building"]:
            device_stats["building"] = building

        battery = safe_int(battery_level)
        if battery is not None and battery < 20:
            device_stats["low_battery"] = True

        if status == "ERROR":
            device_stats["error_count"] += 1

        reading = safe_float(value)
        if sensor_type == "temperature" and reading is not None and reading > 32:
            device_stats["high_temp_count"] += 1

    return dict(stats)


def load_csv_rows(input_path):
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def split_chunks(rows, num_chunks):
    if not rows:
        return []

    chunk_size = max(1, math.ceil(len(rows) / num_chunks))
    return [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]


def build_abnormal_rows(global_stats):
    """
    Build final abnormal-device rows.

    If a device has multiple abnormal reasons, this writes one row per reason.
    You may adapt this behavior if your report explains a different convention.
    """
    output_rows = []

    for device_id, s in global_stats.items():
        building = s["building"]

        if s["low_battery"]:
            output_rows.append((device_id, building, "low battery"))

        if s["error_count"] >= 3:
            output_rows.append((device_id, building, "repeated errors"))

        if s["high_temp_count"] >= 3:
            output_rows.append((device_id, building, "repeated high temperature"))

    return sorted(output_rows, key=lambda row: (row[0], row[2]))


def write_output(output_path, rows):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["device_id", "building", "reason"])
        writer.writerows(rows)


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python3 ray/abnormal_device_detection.py "
            "<input_csv> <output_csv> [num_chunks]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    num_chunks = int(sys.argv[3]) if len(sys.argv) >= 4 else max(2, (os.cpu_count() or 2))

    rows = load_csv_rows(input_path)
    chunks = split_chunks(rows, num_chunks)

    ray.init(ignore_reinit_error=True)

    futures = [process_rows.remote(chunk) for chunk in chunks]
    partial_results = ray.get(futures)

    global_stats = defaultdict(lambda: {
        "building": "",
        "low_battery": False,
        "error_count": 0,
        "high_temp_count": 0,
    })

    for partial in partial_results:
        combine_device_stats(global_stats, partial)

    abnormal_rows = build_abnormal_rows(global_stats)
    write_output(output_path, abnormal_rows)

    print(f"Wrote {len(abnormal_rows)} abnormal-device rows to {output_path}")
    ray.shutdown()


if __name__ == "__main__":
    main()
