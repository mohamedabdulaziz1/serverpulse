
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import psutil


CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80"))
MEMORY_THRESHOLD = float(os.getenv("MEMORY_THRESHOLD", "80"))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD", "80"))
CHECK_URL = os.getenv("CHECK_URL", "")


def collect_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }


def check_endpoint(url):
    if not url:
        return {"configured": False, "status": "skipped"}

    try:
        request = urllib.request.Request(
            url, method="GET"
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            return {
                "configured": True,
                "status": "up" if response.status < 400 else "down",
                "http_status": response.status,
            }
    except Exception as exc:
        return {
            "configured": True,
            "status": "down",
            "error": str(exc),
        }


def main():
    metrics = collect_metrics()
    endpoint = check_endpoint(CHECK_URL)

    warnings = []

    if metrics["cpu_percent"] >= CPU_THRESHOLD:
        warnings.append("CPU usage above threshold")

    if metrics["memory_percent"] >= MEMORY_THRESHOLD:
        warnings.append("Memory usage above threshold")

    if metrics["disk_percent"] >= DISK_THRESHOLD:
        warnings.append("Disk usage above threshold")

    if endpoint["status"] == "down":
        warnings.append("HTTP endpoint is unavailable")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": os.uname().nodename,
        "metrics": metrics,
        "endpoint": endpoint,
        "status": "unhealthy" if warnings else "healthy",
        "warnings": warnings,
    }

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "report.json"
    output_file.write_text(json.dumps(report, indent=2) + "\n")

    print(json.dumps(report, indent=2))

    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
