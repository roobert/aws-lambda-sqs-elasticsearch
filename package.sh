#!/usr/bin/env bash

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_DIR=${PROJECT_ROOT}

deactivate  > /dev/null 2>&1

if [ -d "venv" ]; then
  rm -rf venv
fi

python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt

PACKAGE_DIR=$(find ${PROJECT_ROOT}/venv -name "site-packages")

cd "${PACKAGE_DIR}"
zip -r9 "${PROJECT_ROOT}/lambda.zip" .

cd "${PROJECT_ROOT}"
zip -g "${PROJECT_ROOT}/lambda.zip" aws-lambda-sqs-elasticsearch.py
