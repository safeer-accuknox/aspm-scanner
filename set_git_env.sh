#!/bin/bash

git config --global --add safe.directory "$(pwd)"

export REPOSITORY_URL=${REPOSITORY_URL:-$(git config --get remote.origin.url 2>/dev/null)}
export REPOSITORY_BRANCH=${REPOSITORY_BRANCH:-$(git rev-parse HEAD 2>/dev/null)}
export REPOSITORY_COMMIT_SHA=${REPOSITORY_COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null)}

# Extract the repository name from the REPOSITORY_URL
export REPOSITORY_NAME=$(basename -s .git $REPOSITORY_URL)
