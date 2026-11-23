# Day 081 — YAML and Configuration Files

[⬅ Day 080](../../08-api-cloud/day-080/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 082 ➡](../../08-api-cloud/day-082/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read and write YAML with PyYAML (`safe_load`, `safe_dump`)
- Work with multi-document YAML such as Kubernetes manifests
- Validate configuration and merge environment overlays (base + prod)

## 2. Topic Explanation

**YAML** ("YAML Ain't Markup Language") is the configuration language of DevOps: Kubernetes manifests, Docker Compose, Ansible playbooks, GitHub Actions, Helm values, CloudFormation...

```yaml
service: orders-api          # key: value  -> dict
replicas: 3                  # int
debug: false                 # bool
ports: [80, 443]             # list (flow style)
env:                         # nested dict (indentation = 2 spaces)
  LOG_LEVEL: INFO
containers:                  # list of dicts (block style with "-")
  - name: app
    image: orders:2.4.1
```

PyYAML (`pip install pyyaml`, imported as `yaml`):
- `yaml.safe_load(text_or_file)` → Python objects. **Always use `safe_load`**: plain `yaml.load` can construct arbitrary Python objects from untrusted files (security risk).
- `yaml.safe_load_all(...)` → iterate over **multi-document** files separated by `---`.
- `yaml.safe_dump(obj, sort_keys=False)` → YAML text.

YAML gotchas: indentation must use **spaces**; `yes/no/on/off` may become booleans in YAML 1.1 (PyYAML) — quote strings like `"on"`; `08` vs `8`; values like `3.10` become floats (quote versions!).

**Overlays:** keep a `base` config and environment-specific overrides (`prod` replicas, `dev` debug), then deep-merge them — the idea behind Kustomize and Helm values files.

## 3. Syntax

```python
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)
docs = list(yaml.safe_load_all(text))
text = yaml.safe_dump(config, sort_keys=False)
```

| Part | Meaning |
|---|---|
| `safe_load` | Parse one YAML document safely. |
| `safe_load_all` | Parse every document separated by `---`. |
| `safe_dump` | Serialise Python data to YAML. |
| `sort_keys=False` | Keep the original key order. |

## 4. Example 1 — Basic Example: YAML ↔ Python

```python
import yaml

text = """
service: orders-api
replicas: 3
debug: false
python_version: "3.10"      # quoted -> stays a string
wrong_version: 3.10         # unquoted -> becomes the float 3.1!
feature_flag: on            # YAML 1.1 turns 'on' into True
ports: [80, 443]
env:
  LOG_LEVEL: INFO
  DB_HOST: db.internal
"""
config = yaml.safe_load(text)
print(type(config).__name__, "with keys", list(config))
print("replicas:", config["replicas"], type(config["replicas"]).__name__)
print("python_version:", repr(config["python_version"]), "| wrong_version:", repr(config["wrong_version"]))
print("feature_flag:", config["feature_flag"])
print("DB host:", config["env"]["DB_HOST"])

config["replicas"] = 5
config["env"]["LOG_LEVEL"] = "DEBUG"
print("--- dumped back to YAML ---")
print(yaml.safe_dump(config, sort_keys=False), end="")
```

## 5. Example 2 — Practical Example: Kubernetes manifests, validation and environment overlays

```python
import copy

import yaml

MANIFESTS = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders
  labels: {app: orders}
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: app
          image: registry.example.com/orders:2.4.1
          resources: {limits: {cpu: 500m, memory: 512Mi}}
        - name: log-shipper
          image: fluent/fluent-bit:latest
---
apiVersion: v1
kind: Service
metadata:
  name: orders
spec:
  ports:
    - port: 80
      targetPort: 8080
"""

docs = list(yaml.safe_load_all(MANIFESTS))
print("Documents:", [f"{d['kind']}/{d['metadata']['name']}" for d in docs])

# Policy checks, like a tiny 'kube-linter'
problems = []
for doc in docs:
    if doc["kind"] != "Deployment":
        continue
    for c in doc["spec"]["template"]["spec"]["containers"]:
        if c["image"].endswith(":latest") or ":" not in c["image"]:
            problems.append(f"{c['name']}: do not use the 'latest' tag")
        if "resources" not in c:
            problems.append(f"{c['name']}: missing resource limits")
print("Policy problems:", problems)


def deep_merge(base, override):
    """Return a new dict: values from override win, nested dicts are merged."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


base_values = yaml.safe_load("""
replicas: 2
image: {repository: orders, tag: "2.4.1"}
env: {LOG_LEVEL: INFO, CACHE_TTL: "60"}
""")
prod_values = yaml.safe_load("""
replicas: 6
env: {LOG_LEVEL: WARNING}
""")
print("--- merged prod values ---")
print(yaml.safe_dump(deep_merge(base_values, prod_values), sort_keys=False), end="")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `safe_load` converts YAML into dicts, lists, ints, bools and strings.
- The gotchas are visible: unquoted `3.10` becomes `3.1` (a float), and `on` becomes `True`. **Quote versions and ambiguous words.**
- After changing values, `safe_dump(..., sort_keys=False)` writes YAML back in the original order.

**Example 2**
- `safe_load_all` returns one Python object per `---` document (a Deployment and a Service).
- Simple policy checks walk the nested structure: `latest` tags and missing resource limits are classic production problems.
- `deep_merge` merges nested dictionaries recursively, so `prod` overrides only `replicas` and `LOG_LEVEL` while keeping `image` and `CACHE_TTL` from the base — exactly how Helm combines `values.yaml` with `values-prod.yaml`.

## 7. Expected Output

**Example 1:**

```text
dict with keys ['service', 'replicas', 'debug', 'python_version', 'wrong_version', 'feature_flag', 'ports', 'env']
replicas: 3 int
python_version: '3.10' | wrong_version: 3.1
feature_flag: True
DB host: db.internal
--- dumped back to YAML ---
service: orders-api
replicas: 5
debug: false
python_version: '3.10'
wrong_version: 3.1
feature_flag: true
ports:
- 80
- 443
env:
  LOG_LEVEL: DEBUG
  DB_HOST: db.internal
```

**Example 2:**

```text
Documents: ['Deployment/orders', 'Service/orders']
Policy problems: ["log-shipper: do not use the 'latest' tag", 'log-shipper: missing resource limits']
--- merged prod values ---
replicas: 6
image:
  repository: orders
  tag: 2.4.1
env:
  LOG_LEVEL: WARNING
  CACHE_TTL: '60'
```

## 8. Common Mistakes

**1. Using `yaml.load` on untrusted input**

It can create arbitrary Python objects. Always use `yaml.safe_load`.

**2. Tabs in YAML**

YAML forbids tabs for indentation → `ScannerError`. Configure your editor to insert spaces.

**3. Unquoted special values**

`version: 1.10` → `1.1`, `country: NO` → `False` (the 'Norway problem'). Quote them.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Load and query:** Load this YAML string and print the names of services with more than 1 replica: `services: [{name: api, replicas: 3}, {name: worker, replicas: 1}, {name: web, replicas: 2}]`.
- **Task 2 (Medium) — Generate a docker-compose file:** Build a Python dict for a docker-compose file with services `web` (nginx:1.27, port 8080:80) and `redis` (redis:7, no ports), dump it with `safe_dump(sort_keys=False)` to `docker-compose.generated.yml`, then read it back and print the service names and images.
- **Task 3 (Practical Challenge) — Config validator:** Write `validate(config)` that checks a loaded app config has `name` (str), `replicas` (int 1–20), `env` in dev/staging/prod and `image` with an explicit non-latest tag. Return a list of errors. Test a valid and an invalid YAML document from one multi-document string.

## 10. DevOps/MLOps Connection

- **DevOps:** generate, lint and transform Kubernetes manifests, Compose files, Ansible inventories and CI workflows; enforce policies in CI before `kubectl apply`.
- **Cloud:** CloudFormation and SAM templates are YAML; Python scripts validate and parameterise them.
- **MLOps:** training configs (`params.yaml` in DVC), MLflow `MLproject` files, KServe/Seldon model manifests and GitHub Actions ML pipelines are YAML.

## 11. Interview Questions

**Q1. Why use `yaml.safe_load` instead of `yaml.load`?**

<details><summary>Show answer</summary>

`safe_load` only builds plain Python types; `load` with the full loader can instantiate arbitrary objects, which is a code-execution risk with untrusted input.

</details>

**Q2. How do you read a multi-document YAML file?**

<details><summary>Show answer</summary>

`yaml.safe_load_all(stream)`, which yields one object per `---` separated document.

</details>

**Q3. What is the 'Norway problem' in YAML?**

<details><summary>Show answer</summary>

Unquoted `NO` (and yes/no/on/off) is parsed as a boolean in YAML 1.1, so country code NO becomes False. Quote such strings.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 81 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 080](../../08-api-cloud/day-080/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 082 ➡](../../08-api-cloud/day-082/README.md)
