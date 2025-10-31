#!/usr/bin/env bash
set -euo pipefail
SUB=${1:-"<sub-id>"}
RG=${2:-"<resource-group>"}
WS=${3:-"<workspace>"}
az account set --subscription "$SUB"
az extension add -n ml -y || true
az configure --defaults group=$RG workspace=$WS
az ml job create -f azureml/job-train.yaml
az ml job create -f azureml/job-register-deploy.yaml
