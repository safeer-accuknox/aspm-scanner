#!/bin/bash

# Either mount a repository to $WORKDIR or provide REPOSITORY_URL to clone.
/clone-helper.sh
CLONE_EXIT_CODE=$?
if [ $CLONE_EXIT_CODE -ne 0 ]; then
    exit $CLONE_EXIT_CODE
fi

# Load Git environment variables
source /set_git_env.sh

set +e  
python /app/main.py
SCAN_EXIT_CODE=$?
set -e  

echo "Status: $SCAN_EXIT_CODE"
exit $SCAN_EXIT_CODE