"""
Day 081 — YAML and Configuration Files
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — YAML ↔ Python
# ======================================================================
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

# ======================================================================
# Example 2 — Kubernetes manifests, validation and environment overlays
# ======================================================================
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
