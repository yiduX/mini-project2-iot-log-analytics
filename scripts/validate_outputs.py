#!/usr/bin/env python3
import csv
from collections import Counter

dataset = "data/iot_logs.csv"

sensor_counts = Counter()
building_warning_error = Counter()
device_counts = Counter()

device_building = {}
low_battery = set()
error_counts = Counter()
high_temp_counts = Counter()

with open(dataset, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sensor_counts[row["sensor_type"]] += 1

        if row["status"] in {"WARNING", "ERROR"}:
            building_warning_error[row["building"]] += 1

        device_id = row["device_id"]
        device_counts[device_id] += 1
        device_building.setdefault(device_id, row["building"])

        try:
            battery = int(float(row["battery_level"]))
            if battery < 20:
                low_battery.add(device_id)
        except ValueError:
            pass

        if row["status"] == "ERROR":
            error_counts[device_id] += 1

        try:
            value = float(row["value"]) if row["value"] else None
            if row["sensor_type"] == "temperature" and value is not None and value > 32:
                high_temp_counts[device_id] += 1
        except ValueError:
            pass

print("===== Expected Sensor Type Counts =====")
for k, v in sorted(sensor_counts.items()):
    print(k, v)

print()
print("===== Expected Warning/Error Counts by Building =====")
for k, v in sorted(building_warning_error.items()):
    print(k, v)

print()
print("===== Expected Top 10 Active Devices =====")
for k, v in sorted(device_counts.items(), key=lambda item: (-item[1], item[0]))[:10]:
    print(k, v)

print()
print("===== Expected Abnormal Device Rows Preview =====")
rows = []
for device_id in device_counts:
    building = device_building.get(device_id, "")
    if device_id in low_battery:
        rows.append((device_id, building, "low battery"))
    if error_counts[device_id] >= 3:
        rows.append((device_id, building, "repeated errors"))
    if high_temp_counts[device_id] >= 3:
        rows.append((device_id, building, "repeated high temperature"))

for row in sorted(rows, key=lambda r: (r[0], r[2]))[:20]:
    print(",".join(row))

print()
print("Expected abnormal-device rows excluding header:", len(rows))
