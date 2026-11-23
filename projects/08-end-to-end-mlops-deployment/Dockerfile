# syntax=docker/dockerfile:1
FROM python:3.12-slim AS train
WORKDIR /build
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt .
RUN pip install -r requirements.txt pyyaml==6.0.2
COPY train.py config.yaml ./
COPY data/ data/
RUN python train.py --config config.yaml

FROM python:3.12-slim AS runtime
LABEL org.opencontainers.image.title="server-failure-api" org.opencontainers.image.version="2.0.0"
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/models/champion.joblib LOG_LEVEL=INFO
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY --from=train /build/models/champion.joblib /build/models/metrics.json ./models/
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).status == 200 else 1)"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
