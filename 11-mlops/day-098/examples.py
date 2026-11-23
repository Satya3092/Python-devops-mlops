"""
Day 098 — Building an ML API using FastAPI
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Input validation with Pydantic + the prediction logic
# ======================================================================
import subprocess
import sys

import joblib
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

# Step 1: make sure a trained model exists (train.py writes models/model.joblib)
result = subprocess.run([sys.executable, "train.py"], capture_output=True, text=True)
print(result.stdout.strip())


class ServerMetrics(BaseModel):
    cpu_usage: float = Field(..., ge=0, le=100)
    memory_usage: float = Field(..., ge=0, le=100)
    disk_usage: float = Field(..., ge=0, le=100)
    error_count: int = Field(..., ge=0)
    response_time_ms: float = Field(..., ge=0)


good = ServerMetrics(cpu_usage=93, memory_usage=91, disk_usage=88, error_count=7, response_time_ms=650)
print("valid input ->", good.model_dump())
try:
    ServerMetrics(cpu_usage=150, memory_usage=91, disk_usage=88, error_count="many", response_time_ms=650)
except ValidationError as error:
    for problem in error.errors():
        print(f"invalid {problem['loc'][0]}: {problem['msg']}")

bundle = joblib.load("models/model.joblib")
frame = pd.DataFrame([good.model_dump()])[bundle["features"]]
probability = bundle["model"].predict_proba(frame)[0, 1]
print(f"prediction -> failure={probability >= bundle['threshold']} probability={probability:.4f} "
      f"model_version={bundle['version']}")

# ======================================================================
# Example 2 — The FastAPI app tested in-process with TestClient
# ======================================================================
import subprocess
import sys

from fastapi.testclient import TestClient

subprocess.run([sys.executable, "train.py"], capture_output=True, check=True)   # ensure the model exists
from app import app                                                            # app.py in this folder

RISKY = {"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}
CALM = {"cpu_usage": 20, "memory_usage": 30, "disk_usage": 40, "error_count": 0, "response_time_ms": 120}

with TestClient(app) as client:                     # 'with' runs the start-up (model loading)
    print("GET /health      ->", client.get("/health").json())
    info = client.get("/model-info").json()
    print("GET /model-info  ->", {k: info[k] for k in ("version", "threshold")}, "| recall:", info["metrics"]["recall"])
    print("POST /predict    ->", client.post("/predict", json=RISKY).json())
    print("POST /predict    ->", client.post("/predict", json=CALM).json())
    bad = client.post("/predict", json={**RISKY, "cpu_usage": 150})
    print("invalid input    ->", bad.status_code, bad.json()["detail"][0]["msg"])
    batch = client.post("/predict/batch", json=[RISKY, CALM]).json()
    print("POST /predict/batch ->", [p["failure"] for p in batch])
    print("OpenAPI paths    ->", sorted(client.get("/openapi.json").json()["paths"]))
