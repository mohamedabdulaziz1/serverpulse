
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPORT_FILE = Path(
    os.getenv("REPORT_FILE", "/app/reports/report.json")
)
PORT = int(os.getenv("HEALTH_PORT", "8080"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_error(404)
            return

        try:
            report = json.loads(REPORT_FILE.read_text())
            healthy = report.get("status") == "healthy"
        except (OSError, json.JSONDecodeError):
            healthy = False

        body = json.dumps({
            "service": "serverpulse",
            "healthy": healthy
        }).encode()

        self.send_response(200 if healthy else 503)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
print(f"Health endpoint listening on port {PORT}", flush=True)
server.serve_forever()
