#!/bin/bash

if mount | grep -q "$WORKDIR"; then
    echo "[INFO] $WORKDIR is mounted. Skipping clone."
    exit 0
fi

if [ -z "$REPOSITORY_URL" ]; then
    echo "[ERROR] No repository mounted at $WORKDIR and REPOSITORY_URL is not set."
    echo "[ERROR] Either mount a repository to $WORKDIR or provide REPOSITORY_URL to clone."
    exit 1
fi

if [ -n "$REPOSITORY_USERNAME" ] && [ -n "$REPOSITORY_ACCESS_TOKEN" ]; then
    FINAL_REPOSITORY_URL="https://$REPOSITORY_USERNAME:$REPOSITORY_ACCESS_TOKEN@$(echo "$REPOSITORY_URL" | awk -F'//' '{print $2}')"
else
    FINAL_REPOSITORY_URL="$REPOSITORY_URL"
fi

if [ -n "$REPOSITORY_BRANCH" ]; then
    echo "[INFO] Cloning branch '$REPOSITORY_BRANCH' from $REPOSITORY_URL into $WORKDIR..."
    git clone --branch "$REPOSITORY_BRANCH" --single-branch "$FINAL_REPOSITORY_URL" "$WORKDIR" 
else
    echo "[INFO] Cloning default branch from $REPOSITORY_URL into $WORKDIR..." 
    git clone "$FINAL_REPOSITORY_URL" "$WORKDIR" 
fi