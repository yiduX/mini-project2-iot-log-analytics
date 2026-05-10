# COMP3006J Mini-Project 2 Starter Package

This package is a **starter implementation and testing scaffold** for Mini-Project 2: Smart Campus IoT Log Analytics.

You still need to:
- Upload the provided dataset to Alibaba Cloud OSS.
- Run the MapReduce jobs in your own environment.
- Run the Ray script in your own environment.
- Verify all outputs yourself.
- Record your actual execution environment, commands, outputs, and runtime evidence.
- Adapt and explain the code in your own report.

## Expected input format

CSV columns:

```text
timestamp,device_id,building,floor,room,sensor_type,event_type,value,status,battery_level
```

## Recommended project structure

```text
mini_project_2/
├── data/
│   └── iot_logs.csv
├── mapreduce/
│   ├── sensor_type_mapper.py
│   ├── sensor_type_reducer.py
│   ├── building_status_mapper.py
│   ├── building_status_reducer.py
│   ├── active_device_mapper.py
│   └── active_device_reducer.py
├── ray/
│   └── abnormal_device_detection.py
├── scripts/
│   ├── run_local_mapreduce_tests.sh
│   └── oss_commands_template.sh
├── outputs/
└── docs/
    └── report_notes_template.md
```

## Alibaba Cloud OSS

Example upload path:

```text
oss://your-bucket-name/miniproject2/input/iot_logs.csv
```

Example upload command:

```bash
aliyun ossutil cp data/iot_logs.csv oss://your-bucket-name/miniproject2/input/iot_logs.csv
```

Example list command:

```bash
aliyun ossutil ls oss://your-bucket-name/miniproject2/input/
```

Do not include your real cloud account details, AccessKey, student name, student ID, group ID, or repository username in the anonymized report.

## Local MapReduce simulation

This does not replace Hadoop/MapReduce evidence, but it helps you debug mapper/reducer logic.

```bash
bash scripts/run_local_mapreduce_tests.sh data/iot_logs.csv
```

The generated files will be placed in `outputs/`.

## Hadoop Streaming pattern

Example pattern for one job:

```bash
hadoop jar /path/to/hadoop-streaming.jar \
  -input /path/to/input/iot_logs.csv \
  -output /path/to/output/sensor_type_count \
  -mapper "python3 sensor_type_mapper.py" \
  -reducer "python3 sensor_type_reducer.py" \
  -file mapreduce/sensor_type_mapper.py \
  -file mapreduce/sensor_type_reducer.py
```

Adapt paths to your actual Hadoop Docker / EC2 / ECS environment.

## Ray abnormal-device detection

Install Ray first:

```bash
pip install ray
```

Run:

```bash
python3 ray/abnormal_device_detection.py data/iot_logs.csv outputs/abnormal_devices.csv
```

The Ray script uses `@ray.remote` tasks and combines partial per-device statistics into one final output.

## Required outputs

MapReduce:
1. `outputs/sensor_type_count.txt`
2. `outputs/warning_error_by_building.txt`
3. `outputs/top10_active_devices.txt`

Ray:
4. `outputs/abnormal_devices.csv`

## Important academic note

Use this package as a starting point. You must understand, test, modify where appropriate, and explain the implementation yourself.
