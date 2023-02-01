#!/bin/ash
set -e

if ! id tmp 2>/dev/null; then
    adduser tmp -D -u $DOCKER_UID
fi

exec su tmp -c "/usr/bin/python3 /status.py"
