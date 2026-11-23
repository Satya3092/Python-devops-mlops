"""
Day 100 — End-to-End Mini MLOps Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Run the training pipeline (steps 1–5)
# ======================================================================
import json
import subprocess
import sys
from pathlib import Path

project = Path("mini-mlops")
result = subprocess.run([sys.executable, "train.py"], cwd=project, capture_output=True, text=True)
print(result.stdout.strip())
print("exit code:", result.returncode)

metrics = json.loads((project / "models" / "metrics.json").read_text())
print("metrics.json:", {k: metrics[k] for k in ("accuracy", "precision", "recall", "roc_auc")})

strict = subprocess.run([sys.executable, "train.py", "--min-recall", "0.99", "--out", "models_strict"],
                        cwd=project, capture_output=True, text=True)
print(strict.stdout.strip().splitlines()[-1])
print("strict gate exit code:", strict.returncode, "(CI would stop here)")

# ======================================================================
# Example 2 — API tests, container build and smoke test (steps 6–11)
# ======================================================================
import shutil
import subprocess
import sys

project = "mini-mlops"


def run(cmd, **kwargs):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=project, capture_output=True, text=True, **kwargs)


run([sys.executable, "train.py"])
tests = run([sys.executable, "-m", "pytest", "-q", "test_app.py"])
print(tests.stdout.strip().splitlines()[-1])

if shutil.which("docker") is None:
    sys.exit("Docker not installed: skipping steps 9-10")
build = run(["docker", "build", "-t", "server-failure-api:1.0.0", "."])
print("build ok" if build.returncode == 0 else build.stderr[-500:])
run(["docker", "rm", "-f", "sfa"])
print(run(["docker", "run", "-d", "--name", "sfa", "-p", "8000:8000", "server-failure-api:1.0.0"]).stdout[:12])
smoke = run([sys.executable, "smoke_test.py"], env={"BASE_URL": "http://127.0.0.1:8000"})
print(smoke.stdout.strip())
print(run(["curl", "-s", "-X", "POST", "http://127.0.0.1:8000/predict", "-H", "Content-Type: application/json",
           "-d", '{"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}']).stdout)
run(["docker", "rm", "-f", "sfa"])
