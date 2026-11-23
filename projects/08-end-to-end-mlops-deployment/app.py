"""
app.py - Project 8: FastAPI service for the champion server-failure model.

Run locally:   uvicorn app:app --reload --port 8000
Docs:          http://127.0.0.1:8000/docs
Metrics:       http://127.0.0.1:8000/metrics  (Prometheus text format)
"""
import logging
import os
import time
from collections import Counter
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

LOG = logging.getLogger("model-api")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s: %(message)s")

MODEL_PATH = Path(os.getenv("MODEL_PATH", Path(__file__).resolve().parent / "models" / "champion.joblib"))
ML = {}                                   # filled at start-up, shared by all requests
REQUESTS = Counter()                      # (path, status) -> count
PREDICTIONS = Counter()                   # "failure" / "ok" -> count
LATENCY = {"seconds": 0.0, "count": 0}    # prediction latency summary


class ServerMetrics(BaseModel):
    """Input features - validated automatically by FastAPI/Pydantic."""
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU utilisation in percent")
    memory_usage: float = Field(..., ge=0, le=100, description="Memory utilisation in percent")
    disk_usage: float = Field(..., ge=0, le=100, description="Disk utilisation in percent")
    error_count: int = Field(..., ge=0, description="Errors in the last 5 minutes")
    response_time_ms: float = Field(..., ge=0, description="Average response time in ms")

    model_config = {"json_schema_extra": {"examples": [
        {"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}
    ]}}


class Prediction(BaseModel):
    failure: bool
    probability: float
    threshold: float
    model_version: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the champion model once at start-up."""
    try:
        ML.update(joblib.load(MODEL_PATH))
        LOG.info("Loaded model v%s (%s) from %s", ML["version"], ML.get("model_type"), MODEL_PATH)
    except FileNotFoundError:
        LOG.error("Model file %s not found - /predict will return 503", MODEL_PATH)
    yield
    ML.clear()


app = FastAPI(title="Server Failure Prediction API", version="2.0.0", lifespan=lifespan)


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    REQUESTS[(request.url.path, response.status_code)] += 1
    if request.url.path.startswith("/predict"):
        LATENCY["seconds"] += elapsed
        LATENCY["count"] += 1
    LOG.info("%s %s -> %s in %.1f ms", request.method, request.url.path, response.status_code, elapsed * 1000)
    return response


@app.get("/health")
def health():
    """Liveness/readiness probe for Docker and Kubernetes."""
    return {"status": "ok" if "model" in ML else "degraded", "model_loaded": "model" in ML}


@app.get("/model-info")
def model_info():
    if "model" not in ML:
        raise HTTPException(status_code=503, detail="model not loaded")
    keys = ("version", "model_type", "trained_at", "features", "threshold", "metrics", "sklearn_version")
    return {key: ML.get(key) for key in keys}


def predict_rows(rows):
    if "model" not in ML:
        raise HTTPException(status_code=503, detail="model not loaded")
    frame = pd.DataFrame([r.model_dump() for r in rows])[ML["features"]]
    probabilities = ML["model"].predict_proba(frame)[:, 1]
    results = [Prediction(failure=bool(p >= ML["threshold"]), probability=round(float(p), 4),
                          threshold=ML["threshold"], model_version=ML["version"]) for p in probabilities]
    PREDICTIONS.update("failure" if r.failure else "ok" for r in results)
    return results


@app.post("/predict", response_model=Prediction)
def predict(metrics: ServerMetrics):
    return predict_rows([metrics])[0]


@app.post("/predict/batch", response_model=list[Prediction])
def predict_batch(items: list[ServerMetrics]):
    if not items or len(items) > 1000:
        raise HTTPException(status_code=422, detail="send between 1 and 1000 items")
    return predict_rows(items)


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """Prometheus text exposition format."""
    lines = ["# TYPE http_requests_total counter"]
    lines += [f'http_requests_total{{path="{p}",status="{s}"}} {n}' for (p, s), n in sorted(REQUESTS.items())]
    lines.append("# TYPE predictions_total counter")
    lines += [f'predictions_total{{outcome="{o}"}} {n}' for o, n in sorted(PREDICTIONS.items())]
    lines.append("# TYPE predict_latency_seconds summary")
    lines.append(f"predict_latency_seconds_sum {LATENCY['seconds']:.6f}")
    lines.append(f"predict_latency_seconds_count {LATENCY['count']}")
    lines.append(f'model_info{{version="{ML.get("version", "none")}"}} 1')
    return "\n".join(lines) + "\n"
