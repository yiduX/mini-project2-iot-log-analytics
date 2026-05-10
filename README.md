
# Smart Campus IoT Log Analytics

This project implements Mini-Project 2 for cloud-based smart campus IoT log analytics. It uses Alibaba Cloud OSS for dataset storage, MapReduce-style processing for baseline analytics, and Ray for parallel abnormal-device detection.

## Project Workflow

```text
IoT log dataset → Alibaba Cloud OSS → MapReduce baseline analytics → Ray extension analytics → comparison
````

## Dataset

The input dataset is a synthetic smart-campus IoT log CSV file with the following fields:

```text
timestamp,device_id,building,floor,room,sensor_type,event_type,value,status,battery_level
```

For privacy and submission requirements, the raw dataset is not included in this repository. Place the dataset locally as:

```text
data/iot_logs.csv
```

## Cloud Storage

The dataset was uploaded to Alibaba Cloud OSS and stored under an anonymised object path:

```text
oss://[anonymous-bucket]/miniproject2/input/iot_logs.csv
```

OSS was used because it provides scalable and durable object storage suitable for batch log analytics.

## MapReduce Baseline Analytics

The `mapreduce/` folder contains mapper and reducer scripts for:

1. Event count by sensor type
2. Warning/error count by building
3. Top 10 most active devices

Run local MapReduce-style tests with:

```bash
bash scripts/run_local_mapreduce_tests.sh data/iot_logs.csv
```

Outputs are written to:

```text
outputs/sensor_type_count.txt
outputs/warning_error_by_building.txt
outputs/top10_active_devices.txt
```

## Ray Extension Analytics

The `ray/` folder contains the Ray abnormal-device detection script. A device is abnormal if it satisfies at least one condition:

* `battery_level < 20`
* `status = ERROR` in at least 3 records
* temperature `value > 32` in at least 3 records

Run:

```bash
python3 ray/abnormal_device_detection.py data/iot_logs.csv outputs/abnormal_devices.csv 4
```

Output:

```text
outputs/abnormal_devices.csv
```

## Validation

An independent validation script recomputes expected results directly from the CSV dataset:

```bash
python3 scripts/validate_outputs.py
```

The validation results were compared with the MapReduce outputs and Ray abnormal-device output.

## Main Results

MapReduce outputs include:

* Sensor type counts
* Warning/error counts by building
* Top 10 active devices

Ray generated:

```text
243 abnormal-device rows
244 CSV lines including the header
```

## Repository Structure

```text
mapreduce/   Mapper and reducer scripts
ray/         Ray abnormal-device detection script
scripts/     Run, OSS, and validation scripts
outputs/     Generated result files
docs/        Report notes and instructions
README.md    Project overview
```

```
```
