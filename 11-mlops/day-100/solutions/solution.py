"""
Day 100 — End-to-End Mini MLOps Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import subprocess
import sys
from pathlib import Path

import yaml

PROJECT = Path("mini-mlops")

# ===== Task 1 =====
subprocess.run([sys.executable, "train.py"], cwd=PROJECT, capture_output=True, check=True)
subprocess.run([sys.executable, "train.py", "--threshold", "0.5", "--out", "models_t50", "--min-recall", "0"],
               cwd=PROJECT, capture_output=True, check=True)
default = json.loads((PROJECT / "models" / "metrics.json").read_text())
strict = json.loads((PROJECT / "models_t50" / "metrics.json").read_text())
print(f"{'threshold':<10}{'precision':>10}{'recall':>8}")
for m in (default, strict):
    print(f"{m['threshold']:<10}{m['precision']:>10}{m['recall']:>8}")

# ===== Task 2 =====
sys.path.insert(0, str(PROJECT))
subprocess.run([sys.executable, "train.py"], cwd=PROJECT, capture_output=True, check=True)
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    info = client.get("/model-info").json()
    print(f"GET /model-info -> version {info['version']}, features {len(info['features'])}, recall {info['metrics']['recall']}")
    batch = [
        {"cpu_usage": 20, "memory_usage": 30, "disk_usage": 40, "error_count": 0, "response_time_ms": 120},
        {"cpu_usage": 95, "memory_usage": 94, "disk_usage": 92, "error_count": 9, "response_time_ms": 700},
        {"cpu_usage": 75, "memory_usage": 85, "disk_usage": 80, "error_count": 4, "response_time_ms": 350},
    ]
    print("batch of 3 ->", [p["failure"] for p in client.post("/predict/batch", json=batch).json()])

# ===== Task 3 =====
workflow = {
    "name": "mini-mlops",
    "on": {"push": {"branches": ["main"]}, "pull_request": {}},
    "jobs": {
        "train-and-test": {
            "runs-on": "ubuntu-latest",
            "defaults": {"run": {"working-directory": "11-mlops/day-100/mini-mlops"}},
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"uses": "actions/setup-python@v5", "with": {"python-version": "3.12"}},
                {"run": "pip install -r requirements-dev.txt"},
                {"run": "python train.py"},
                {"run": "pytest -q"},
                {"uses": "actions/upload-artifact@v4",
                 "with": {"name": "metrics", "path": "11-mlops/day-100/mini-mlops/models/metrics.json"}},
            ],
        },
        "docker": {
            "needs": "train-and-test",
            "runs-on": "ubuntu-latest",
            "defaults": {"run": {"working-directory": "11-mlops/day-100/mini-mlops"}},
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"run": "docker build -t server-failure-api:${{ github.sha }} ."},
                {"run": "docker run -d --name sfa -p 8000:8000 server-failure-api:${{ github.sha }}"},
                {"run": "pip install requests && BASE_URL=http://127.0.0.1:8000 python smoke_test.py"},
            ],
        },
    },
}
text = yaml.safe_dump(workflow, sort_keys=False)
print(text, end="")
