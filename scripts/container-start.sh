#!/usr/bin/env bash
set -u

cd /app || exit

python monitor.py || true

(
    while true; do
        sleep "${CHECK_INTERVAL:-60}"
        python monitor.py || true
    done
) &

exec python health_server.py
