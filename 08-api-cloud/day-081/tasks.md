# Day 081 — Practice Tasks: YAML and Configuration Files

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Load and query

**Problem statement:** Load this YAML string and print the names of services with more than 1 replica: `services: [{name: api, replicas: 3}, {name: worker, replicas: 1}, {name: web, replicas: 2}]`.

**Input requirements:** No user input required.

**Expected behavior:** `['api', 'web']`.

**Expected output:**

```text
['api', 'web']
```

## Task 2 — Medium: Generate a docker-compose file

**Problem statement:** Build a Python dict for a docker-compose file with services `web` (nginx:1.27, port 8080:80) and `redis` (redis:7, no ports), dump it with `safe_dump(sort_keys=False)` to `docker-compose.generated.yml`, then read it back and print the service names and images.

**Input requirements:** No user input required.

**Expected behavior:** The YAML text and the two services.

**Expected output:**

```text
services:
  web:
    image: nginx:1.27
    ports:
    - 8080:80
  redis:
    image: redis:7
web -> nginx:1.27
redis -> redis:7
```

## Task 3 — Practical Challenge: Config validator

**Problem statement:** Write `validate(config)` that checks a loaded app config has `name` (str), `replicas` (int 1–20), `env` in dev/staging/prod and `image` with an explicit non-latest tag. Return a list of errors. Test a valid and an invalid YAML document from one multi-document string.

**Input requirements:** No user input required.

**Expected behavior:** Valid config → no errors; invalid → four errors.

**Expected output:**

```text
orders -> valid
42 -> ['name must be a string', 'replicas must be an int between 1 and 20', 'env must be dev, staging or prod', 'image needs an explicit, non-latest tag']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
