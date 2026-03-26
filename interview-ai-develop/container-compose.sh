#!/bin/bash
if command -v docker-compose &> /dev/null; then
    CMD="docker-compose"
elif command -v podman-compose &> /dev/null; then
    CMD="podman-compose"
elif docker compose version &> /dev/null; then
    CMD="docker compose"
else
    echo "Error: No docker/podman tool found."
    exit 1
fi
echo "Using command: $CMD"
$CMD -f docker-compose.yml "$@"