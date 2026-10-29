#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$PROJECT_DIR/reports"
BACKUP_DIR="$PROJECT_DIR/backups"

mkdir -p "$BACKUP_DIR"

timestamp="$(date '+%Y%m%d-%H%M%S')"
archive="$BACKUP_DIR/serverpulse-$timestamp.tar.gz"

files=()

for file in report.json monitor.log; do
    if [[ -f "$REPORT_DIR/$file" ]]; then
        files+=("$file")
    fi
done

if [[ ${#files[@]} -eq 0 ]]; then
    echo "ERROR: No reports available to back up."
    exit 1
fi

tar -czf "$archive" -C "$REPORT_DIR" "${files[@]}"

echo "Backup created: $archive"
