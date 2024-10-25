#!/usr/bin/env bash
# Exit when any command fails
set -euo pipefail

if [ -s /workspace/changed_folders ]; then
    CLEAN_BRANCH_NAME=$(cat /workspace/clean_branch_name)
    while IFS="" read -r PIPELINE_NAME || [ -n "$PIPELINE_NAME" ]
    do
        echo "##### Building JSON specificaton file for $PIPELINE_NAME Docker image #####"
        TEMPLATE_NAME=${PIPELINE_NAME}-${CLEAN_BRANCH_NAME}-${CI_SERVICE_NAME}

        gcloud dataflow flex-template build "gs://$DATAFLOW_BUCKET/$TEMPLATE_NAME.json" \
        --image "$LOCATION-docker.pkg.dev/$PROJECT_ID/$DOCKER_REPO_NAME/$TEMPLATE_NAME:latest" \
        --sdk-language "$SDK_LANGUAGE"
        #--metadata-file "$METADATA_FILE"
    done < /workspace/changed_folders
else
    echo "##### No changes to pipeline code detected #####"
fi