# Day 099 — Practice Tasks: Dockerizing an ML Application

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Inspect the Dockerfile

**Problem statement:** Parse `Dockerfile` and print every instruction keyword with its count (FROM, RUN, COPY, ENV, ...), plus all exposed ports and environment variables.

**Input requirements:** No user input required.

**Expected behavior:** Instruction counts, `['8000']` and the ENV variable names.

**Expected output:**

```text
{'FROM': 2, 'WORKDIR': 2, 'ENV': 2, 'COPY': 6, 'RUN': 4, 'LABEL': 1, 'USER': 1, 'EXPOSE': 1, 'HEALTHCHECK': 1, 'CMD': 2}
EXPOSE: ['8000']
ENV vars: ['LOG_LEVEL', 'MODEL_PATH', 'PIP_NO_CACHE_DIR', 'PYTHONDONTWRITEBYTECODE', 'PYTHONUNBUFFERED']
```

## Task 2 — Medium: Image size budget

**Problem statement:** Write `check_image_size(size_text, budget_mb)` that converts Docker size strings (`"512MB"`, `"1.2GB"`, `"850kB"`) to MB and returns `OK`/`TOO BIG`. Test with several values and a 600 MB budget.

**Input requirements:** No user input required.

**Expected behavior:** Converted sizes and verdicts.

**Expected output:**

```text
512MB -> (512.0, 'OK')
1.2GB -> (1200.0, 'TOO BIG')
850kB -> (0.8, 'OK')
601MB -> (601.0, 'TOO BIG')
```

## Task 3 — Practical Challenge: Generate a Compose file

**Problem statement:** Using PyYAML, generate `docker-compose.yml` for the API with a build context, image tag, port 8000, `LOG_LEVEL` env var, `restart: unless-stopped` and resource limits (1 CPU, 512M). Print it and the command to start it.

**Input requirements:** No user input required.

**Expected behavior:** A valid Compose YAML.

**Expected output:**

```text
services:
  api:
    build: .
    image: server-failure-api:1.0.0
    ports:
    - 8000:8000
    environment:
      LOG_LEVEL: INFO
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
Wrote docker-compose.yml -> run: docker compose up -d --build
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
