#!/usr/bin/env bash
# Exit when any command fails
set -euo pipefail

if [[ -z "$1" || ! "$1" =~ ^(batch|streaming)$ ]]; then
  echo "Error: Invalid argument. Usage: $0 (batch|streaming)"
  exit 1
fi

MODE=$1 # batch or streaming
PROJECT=pure-chariot-438814-i0
LOCATION=europe-west1
PIPELINE=${PWD##*/}  
BUCKET=dataflow-templates-artifacts
ENV=develop
CI_FILE_CONTENT=$(cat ci/$MODE/${ENV}_parameters.txt | sed 's/--parameters /--/g')

# Use DirectRunner first for quick development and testing
# Currently, using DataflowRunner in local with a python package doesn't work.
python3 -m main \
  --project="$PROJECT" \
  --job_name="local-$PIPELINE-`date +%Y-%m-%d-%H%M%S`" \
  --runner=DirectRunner \
  --region "$LOCATION" \
  --setup_file ./setup.py \
  --temp_location "gs://$BUCKET/temp" \
  --staging_location "gs://$BUCKET/staging" $(echo $CI_FILE_CONTENT)
  
