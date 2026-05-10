#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-data/iot_logs.csv}"

if [ ! -f "$INPUT" ]; then
  echo "Input file not found: $INPUT" >&2
  echo "Usage: bash scripts/run_local_mapreduce_tests.sh data/iot_logs.csv" >&2
  exit 1
fi

mkdir -p outputs

python3 mapreduce/sensor_type_mapper.py < "$INPUT" \
  | sort \
  | python3 mapreduce/sensor_type_reducer.py \
  > outputs/sensor_type_count.txt

python3 mapreduce/building_status_mapper.py < "$INPUT" \
  | sort \
  | python3 mapreduce/building_status_reducer.py \
  > outputs/warning_error_by_building.txt

python3 mapreduce/active_device_mapper.py < "$INPUT" \
  | sort \
  | python3 mapreduce/active_device_reducer.py \
  > outputs/top10_active_devices.txt

echo "Generated:"
echo "  outputs/sensor_type_count.txt"
echo "  outputs/warning_error_by_building.txt"
echo "  outputs/top10_active_devices.txt"
