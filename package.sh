#!/usr/bin/env bash

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_DIR=${PROJECT_ROOT}
SHIPPER_DIR=${PROJECT_ROOT}/aws-lambda-sqs-elasticsearch
PACKAGE_DIR=$(find ${PROJECT_ROOT}/venv -name "site-packages")

deactivate  > /dev/null 2>&1

if [ -d "venv" ]; then
  rm -rf venv
fi

python3 -m venv venv
. venv/bin/activate
pip3 install -r <(pip3 freeze)

cd "${PACKAGE_DIR}"
zip -r9 "${TARGET_DIR}/lambda.zip" .

cd "${SHIPPER_DIR}"
zip -g "${TARGET_DIR}/lambda.zip" aws-lambda-sqs-elasticsearch.py
