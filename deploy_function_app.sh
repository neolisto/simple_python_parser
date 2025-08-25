#! /bin/bash

RG=$1
FUNCTION_APP_NAME=$2

rm -rf ./.python_packages || true
rm function_app.zip || true

pip install -r requirements.txt --target="./.python_packages/lib/site-packages"

zip function_app.zip function_app.py function.json host.json
az functionapp deployment source config-zip --build-remote false -g $RG -n $FUNCTION_APP_NAME --src function_app.zip