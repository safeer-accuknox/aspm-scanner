#!/bin/bash

# Load Git environment variables
source /set_git_env.sh

set +e  
python /app/main.py
SCAN_EXIT_CODE=$?
set -e  

echo "Status: $SCAN_EXIT_CODE"
exit $SCAN_EXIT_CODE