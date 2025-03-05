#!/bin/bash

cd $PWD
git config --global --add safe.directory "$(pwd)"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then


    export REPOSITORY_URL=${REPOSITORY_URL:-$(git config --get remote.origin.url | sed -E 's#(https?://)[^/@]+@#\1#')} # remove the oath vars from git remote URL
    export REPOSITORY_BRANCH=${REPOSITORY_BRANCH:-$(git rev-parse --abbrev-ref HEAD)}
    export REPOSITORY_COMMIT_SHA=${REPOSITORY_COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null)}

    # Extract the repository name from the REPOSITORY_URL
    export REPOSITORY_NAME=$(basename -s .git $REPOSITORY_URL)
fi