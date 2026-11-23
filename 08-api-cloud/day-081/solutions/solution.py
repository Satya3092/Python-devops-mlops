"""
Day 081 — YAML and Configuration Files: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
from pathlib import Path

import yaml

# ===== Task 1 =====
data = yaml.safe_load("services: [{name: api, replicas: 3}, {name: worker, replicas: 1}, {name: web, replicas: 2}]")
print([s["name"] for s in data["services"] if s["replicas"] > 1])

# ===== Task 2 =====
compose = {
    "services": {
        "web": {"image": "nginx:1.27", "ports": ["8080:80"]},
        "redis": {"image": "redis:7"},
    }
}
text = yaml.safe_dump(compose, sort_keys=False)
Path("docker-compose.generated.yml").write_text(text)
print(text, end="")
loaded = yaml.safe_load(Path("docker-compose.generated.yml").read_text())
for name, svc in loaded["services"].items():
    print(name, "->", svc["image"])

# ===== Task 3 =====
def validate(config):
    errors = []
    if not isinstance(config.get("name"), str):
        errors.append("name must be a string")
    replicas = config.get("replicas")
    if not isinstance(replicas, int) or not 1 <= replicas <= 20:
        errors.append("replicas must be an int between 1 and 20")
    if config.get("env") not in ("dev", "staging", "prod"):
        errors.append("env must be dev, staging or prod")
    image = str(config.get("image", ""))
    if ":" not in image or image.endswith(":latest"):
        errors.append("image needs an explicit, non-latest tag")
    return errors


docs = yaml.safe_load_all("""
name: orders
replicas: 3
env: prod
image: orders:2.4.1
---
name: 42
replicas: "three"
env: production
image: orders:latest
""")
for doc in docs:
    print(doc.get("name"), "->", validate(doc) or "valid")
