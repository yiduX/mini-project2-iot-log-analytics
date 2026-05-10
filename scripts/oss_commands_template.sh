#!/usr/bin/env bash 
set -euo pipefail

BUCKET="comp3006j-mini-project2-18"
LOCAL_DATASET="data/iot_logs.csv"
OSS_PATH="oss://${BUCKET}/miniproject2/input/iot_logs.csv"

echo "Uploading dataset to Alibaba Cloud OSS..."
ossutil cp "${LOCAL_DATASET}" "${OSS_PATH}"

echo "Listing uploaded object..."
ossutil ls "oss://${BUCKET}/miniproject2/input/"
