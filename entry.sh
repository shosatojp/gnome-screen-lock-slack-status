#!/bin/ash
set -e

if ! id tmp 2>/dev/null; then
    adduser tmp -u $DOCKER_UID -D
fi

su tmp -c "/usr/bin/python3 /status.py"
