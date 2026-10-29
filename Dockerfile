
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HEALTH_PORT=8080 \
    CHECK_INTERVAL=60

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY monitor.py health_server.py ./
COPY scripts/container-start.sh ./scripts/container-start.sh

RUN useradd --create-home appuser \
    && mkdir -p /app/reports \
    && chown -R appuser:appuser /app/reports \
    && chmod +x /app/scripts/container-start.sh

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s \
    --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=3)"

CMD ["/app/scripts/container-start.sh"]
