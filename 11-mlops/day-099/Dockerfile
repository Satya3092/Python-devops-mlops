# syntax=docker/dockerfile:1
# ---------- Stage 1: train the model inside the SAME environment used to serve it ----------
FROM python:3.12-slim AS train
WORKDIR /build
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY train.py .
COPY data/ data/
RUN python train.py --out /build/models

# ---------- Stage 2: small runtime image with only what is needed to serve ----------
FROM python:3.12-slim AS runtime
LABEL org.opencontainers.image.title="server-failure-api" \
      org.opencontainers.image.description="FastAPI service predicting server failures"
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/models/model.joblib LOG_LEVEL=INFO
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY --from=train /build/models ./models
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).status == 200 else 1)"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
