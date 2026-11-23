# Day 098 — Building an ML API using FastAPI

[⬅ Day 097](../../11-mlops/day-097/README.md) | [📚 Phase 11: MLOps Foundation](../README.md) | [🏠 Home](../../README.md) | [Day 099 ➡](../../11-mlops/day-099/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 11 — MLOps Foundation | 🔴 Advanced beginner (MLOps) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Build a REST API with FastAPI: routes, path/query parameters and JSON bodies
- Validate prediction input with Pydantic models and return typed responses
- Load a model once at start-up, expose `/health` and `/predict`, and test with `TestClient`

## 2. Topic Explanation

A trained model is only useful when other systems can call it. The standard way is an **HTTP API**: clients `POST` features as JSON to `/predict` and receive a prediction (Days 76–80 from the other side!).

**FastAPI** is a modern Python web framework ideal for ML APIs:
- Very fast (built on Starlette + uvicorn, async).
- Uses **type hints + Pydantic** to validate requests automatically — invalid input gets a clear **422** error before your code runs.
- Generates interactive docs at `/docs` (Swagger UI) and `/openapi.json`.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Features(BaseModel):
    cpu_usage: float = Field(ge=0, le=100)

@app.post("/predict")
def predict(features: Features):
    return {"failure": features.cpu_usage > 90}
```

Run it with **uvicorn** (an ASGI server): `uvicorn app:app --reload --port 8000`.

**Production patterns used in [`app.py`](app.py):**
- **Load the model once** at start-up (`lifespan`), not per request.
- `/health` endpoint for Docker/Kubernetes probes; `/model-info` for debugging which model is live.
- **Pydantic** input model with ranges (`ge`, `le`) = data validation at the edge.
- Typed `response_model` so the API contract is documented and enforced.
- Batch endpoint for efficiency; request-logging middleware with latency.
- `503` when the model is missing instead of crashing.

Files in this folder: [`train.py`](train.py) (creates `models/model.joblib`), [`app.py`](app.py) (the API), [`test_app.py`](test_app.py) (pytest tests).

> Install: `pip install scikit-learn pandas joblib fastapi uvicorn httpx pydantic`. Run commands from inside this day's folder.

## 3. Syntax

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="My API")

class Item(BaseModel):
    value: float = Field(..., ge=0)

@app.get("/items/{item_id}")              # path parameter
def read(item_id: int, verbose: bool = False):   # query parameter ?verbose=true
    ...

@app.post("/predict", response_model=Output)
def predict(item: Item):                   # JSON body validated by Pydantic
    raise HTTPException(status_code=503, detail="...")
```

| Part | Meaning |
|---|---|
| `@app.get / @app.post` | Route decorators: method + path. |
| `path / query params` | Typed function arguments become URL parameters. |
| `BaseModel body` | Request JSON validated against the model; errors → 422. |
| `response_model` | Shapes and documents the response. |
| `HTTPException` | Return an error status with a message. |

## 4. Example 1 — Basic Example: Input validation with Pydantic + the prediction logic

```python
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
```

## 5. Example 2 — Practical Example: The FastAPI app tested in-process with TestClient

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `train.py` produces `models/model.joblib` (Day 97 bundle) — run it once before starting the API.
- The Pydantic model validates types **and** ranges. Bad input produces precise error messages (this is exactly what FastAPI returns as a 422 response).
- The prediction logic: build a one-row DataFrame in the model's feature order → `predict_proba` → apply the threshold.

**Example 2 — `app.py` walkthrough**
- `lifespan` loads the bundle once at start-up into `ML`; if the file is missing the app still starts and `/predict` returns **503** (a readiness probe would keep traffic away).
- `ServerMetrics` (request) and `Prediction` (response) models define the API contract; FastAPI uses them for validation **and** for the `/docs` page.
- The middleware logs method, path, status and latency for every request.
- `TestClient` calls the app in-process (no server needed) — perfect for unit tests in CI. Using it in a `with` block triggers the start-up event.
- Run it for real with `uvicorn app:app --port 8000` and open `http://127.0.0.1:8000/docs`.

## 7. Expected Output

**Example 1:**

```text
[data] server_failures.csv: 400 rows -> 400 after cleaning, failure rate 18.5%
[eval] accuracy=0.91 precision=0.6957 recall=0.8889 f1=0.7805 roc_auc=0.981
[gate] passed: recall 0.8889 >= 0.8
[save] models/model.joblib (2.2 KB), metrics.json
valid input -> {'cpu_usage': 93.0, 'memory_usage': 91.0, 'disk_usage': 88.0, 'error_count': 7, 'response_time_ms': 650.0}
invalid cpu_usage: Input should be less than or equal to 100
invalid error_count: Input should be a valid integer, unable to parse string as an integer
prediction -> failure=True probability=0.9981 model_version=1.0.0
```

**Example 2:**

```text
GET /health      -> {'status': 'ok', 'model_loaded': True}
GET /model-info  -> {'version': '1.0.0', 'threshold': 0.3} | recall: 0.8889
POST /predict    -> {'failure': True, 'probability': 0.9981, 'threshold': 0.3, 'model_version': '1.0.0'}
POST /predict    -> {'failure': False, 'probability': 0.0001, 'threshold': 0.3, 'model_version': '1.0.0'}
invalid input    -> 422 Input should be less than or equal to 100
POST /predict/batch -> [True, False]
OpenAPI paths    -> ['/health', '/model-info', '/predict', '/predict/batch']
```

> ℹ️ Example 2 and Tasks 2–3 need FastAPI and httpx installed. The probabilities depend on your scikit-learn version.

## 8. Common Mistakes

**1. Loading the model inside the endpoint**

Loading on every request adds hundreds of ms and memory churn. Load once at start-up.

**2. No input validation**

Without Pydantic ranges, `cpu_usage: -500` reaches the model and returns nonsense. Validate at the edge.

**3. Different feature order**

Build the input DataFrame with the saved `features` list so the columns always match training.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Pydantic model:** Create a Pydantic model `Deployment` with `service` (str, min length 3), `replicas` (int 1–50) and `env` (one of dev/staging/prod using `Literal`). Validate one good and one bad payload and print the errors.
- **Task 2 (Medium) — Your first FastAPI app:** Write a small FastAPI app with `GET /ping`, `GET /servers/{name}` (404 via `HTTPException` when unknown) and `GET /servers?env=...` (query parameter). Test all routes with `TestClient`.
- **Task 3 (Practical Challenge) — Run the test suite:** Run `pytest -q test_app.py` from Python with `subprocess` and print the summary line. Then add (in your own copy) a test that `/model-info` returns the five feature names.

## 10. DevOps/MLOps Connection

- **DevOps:** the API is a normal web service — containerise it (Day 99), put it behind a load balancer/ingress, add health probes, logging, metrics and autoscaling.
- **Cloud:** deploy on ECS/EKS, App Runner, or Lambda (with an adapter); API Gateway adds auth and rate limits (Day 80 skills).
- **MLOps:** this is **online inference** (real-time). The other pattern, **batch inference**, is Day 97's `predict_from_file`. Monitoring request latency and prediction distributions here is how you detect model drift.

## 11. Interview Questions

**Q1. Why is FastAPI popular for serving ML models?**

<details><summary>Show answer</summary>

High performance (ASGI), automatic request validation with Pydantic, automatic OpenAPI docs, and simple Python type-hint based code.

</details>

**Q2. Where should you load the model in a web API and why?**

<details><summary>Show answer</summary>

Once at start-up (lifespan/startup event), so requests don't pay the loading cost and memory isn't duplicated.

</details>

**Q3. What HTTP status does FastAPI return for invalid request bodies?**

<details><summary>Show answer</summary>

422 Unprocessable Entity, with details about each validation error.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 98 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 097](../../11-mlops/day-097/README.md) | [📚 Phase 11: MLOps Foundation](../README.md) | [🏠 Home](../../README.md) | [Day 099 ➡](../../11-mlops/day-099/README.md)
