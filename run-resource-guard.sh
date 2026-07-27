#!/usr/bin/env bash
# RESOURCE GUARD — macOS / Linux launcher.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
"$PY" -c "import psutil" 2>/dev/null || "$PY" -m pip install --user psutil
exec "$PY" resource_guard.py "$@"
