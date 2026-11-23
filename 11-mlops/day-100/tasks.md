# Day 100 — Practice Tasks: End-to-End Mini MLOps Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Retrain with a new threshold

**Problem statement:** Run `train.py` with `--threshold 0.5 --out models_t50` and compare its precision/recall with the default (0.3) run by reading both `metrics.json` files.

**Input requirements:** No user input required.

**Expected behavior:** A side-by-side comparison: higher threshold → higher precision, lower recall.

**Expected output:**

```text
threshold  precision  recall
0.3           0.6957  0.8889
0.5           0.7895  0.8333
```

## Task 2 — Medium: Model info and batch predictions

**Problem statement:** Using `TestClient` on `mini-mlops/app.py`, print the model version, number of features and recall from `/model-info`, then send a batch of 3 servers (calm, risky, borderline) to `/predict/batch` and print the failure flags.

**Input requirements:** No user input required.

**Expected behavior:** Model info and three predictions.

**Expected output:**

```text
GET /model-info -> version 1.0.0, features 5, recall 0.8889
batch of 3 -> [False, True, True]
```

## Task 3 — Practical Challenge: Write the GitHub Actions workflow

**Problem statement:** Generate (as YAML via PyYAML) a CI workflow `.github/workflows/mlops.yml` for the mini project with jobs: `train-and-test` (checkout, setup-python 3.12, install dev requirements, `python train.py`, `pytest -q`, upload `models/metrics.json` as an artefact) and `docker` (needs the first job; `docker build`, run container, smoke test). Print the YAML. (A complete version is in Project 8.)

**Input requirements:** No user input required.

**Expected behavior:** A valid workflow YAML with two jobs.

**Expected output:**

```text
name: mini-mlops
'on':
  push:
    branches:
    - main
  pull_request: {}
jobs:
  train-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: 11-mlops/day-100/mini-mlops
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - run: pip install -r requirements-dev.txt
    - run: python train.py
    - run: pytest -q
    - uses: actions/upload-artifact@v4
      with:
        name: metrics
        path: 11-mlops/day-100/mini-mlops/models/metrics.json
  docker:
    needs: train-and-test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: 11-mlops/day-100/mini-mlops
    steps:
    - uses: actions/checkout@v4
    - run: docker build -t server-failure-api:${{ github.sha }} .
    - run: docker run -d --name sfa -p 8000:8000 server-failure-api:${{ github.sha
        }}
    - run: pip install requests && BASE_URL=http://127.0.0.1:8000 python smoke_test.py
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
