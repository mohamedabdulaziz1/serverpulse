#!/usr/bin/env bash

set -u

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$PROJECT_DIR/.venv/bin/python"
LOG_DIR="$PROJECT_DIR/reports"
LOG_FILE="$LOG_DIR/monitor.log"

mkdir -p "$LOG_DIR"

if [[ ! -x "$PYTHON" ]]; then
    echo "ERROR: Python virtual environment not found."
    echo "Run: python3 -m venv .venv"
    exit 2
fi

timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

echo "[$timestamp] Starting ServerPulse" | tee -a "$LOG_FILE"

"$PYTHON" "$PROJECT_DIR/monitor.py" >> "$LOG_FILE" 2>&1
status=$?

timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

if [[ "$status" -eq 0 ]]; then
    echo "[$timestamp] Result: HEALTHY" | tee -a "$LOG_FILE"
else
    echo "[$timestamp] Result: FAILED (exit code $status)" | tee -a "$LOG_FILE"
fi

exit "$status"

