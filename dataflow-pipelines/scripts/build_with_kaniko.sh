#!/busybox/sh
# Exit when any command fails
set -euo pipefail

if [ -s /workspace/changed_folders ]; then
    CLEAN_BRANCH_NAME=$(cat /workspace/clean_branch_name)
    while IFS="" read -r PIPELINE_NAME || [ -n "$PIPELINE_NAME" ]
    do
        cd ../$PIPELINE_NAME
        echo "##### Building Dataflow Docker image $PIPELINE_NAME with Kaniko"#####
        TEMPLATE_NAME=${PIPELINE_NAME}-${CLEAN_BRANCH_NAME}-${CI_SERVICE_NAME}

        /kaniko/executor \
        --cache=true \
        --destination="$LOCATION-docker.pkg.dev/$PROJECT_ID/$DOCKER_REPO_NAME/$TEMPLATE_NAME:latest" \
        --build-arg "PIPELINE_NAME=$PIPELINE_NAME"

        # Go back to the root directory before processing the next folder
        cd - > /dev/null
    done < /workspace/changed_folders
else
    echo "##### No changes to pipeline code detected #####"
fi