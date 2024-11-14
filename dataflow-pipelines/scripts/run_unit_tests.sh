#!/bin/bash
# Exit when any command fails
set -euo pipefail

if [ -s /workspace/changed_folders ]; then

    while IFS="" read -r PIPELINE_NAME || [ -n "$PIPELINE_NAME" ]
    do
        cd ../$PIPELINE_NAME
        echo "##### Running unit tests for $PIPELINE_NAME #####"

        # Check if the 'tests' folder exists and is not empty
        if [[ -d tests && -n $(ls -A tests) ]]; then
        for file in $(find tests -type f); do
            file_name=$(basename "$file")
            if [[$file_name == test*.py]]
                # Run tests for each Python file found
                echo "Running tests for $file_name"
                python -m tests.$file_name
            fi
        done
        else
        echo "#### No Python files found in the 'tests' directory ####"
        fi

        # Go back to the root directory before processing the next folder
        cd - > /dev/null
    done < /workspace/changed_folders
else
    echo "##### No changes to pipeline code detected #####"
fi