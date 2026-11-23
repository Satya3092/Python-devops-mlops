"""
Day 099 — Dockerizing an ML Application: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import re
from collections import Counter
from pathlib import Path

import yaml

# ===== Task 1 =====
lines = [l.strip() for l in Path("Dockerfile").read_text().splitlines() if l.strip() and not l.strip().startswith("#")]
keywords = Counter(l.split()[0] for l in lines if l.split()[0].isupper())
print(dict(keywords))
print("EXPOSE:", [l.split()[1] for l in lines if l.startswith("EXPOSE")])
env_text = " ".join(l for l in lines if l.startswith("ENV") or "=" in l and not l.startswith(("RUN", "CMD", "LABEL", "HEALTHCHECK", "FROM", "COPY")))
print("ENV vars:", sorted(set(re.findall(r"([A-Z_]+)=", env_text))))

# ===== Task 2 =====
def check_image_size(size_text, budget_mb):
    number, unit = re.match(r"([\d.]+)\s*([kKMG]B)", size_text).groups()
    mb = float(number) * {"kB": 1 / 1000, "KB": 1 / 1000, "MB": 1, "GB": 1000}[unit]
    return round(mb, 1), "OK" if mb <= budget_mb else "TOO BIG"


for size in ["512MB", "1.2GB", "850kB", "601MB"]:
    print(size, "->", check_image_size(size, 600))

# ===== Task 3 =====
compose = {
    "services": {
        "api": {
            "build": ".",
            "image": "server-failure-api:1.0.0",
            "ports": ["8000:8000"],
            "environment": {"LOG_LEVEL": "INFO"},
            "restart": "unless-stopped",
            "deploy": {"resources": {"limits": {"cpus": "1.0", "memory": "512M"}}},
        }
    }
}
text = yaml.safe_dump(compose, sort_keys=False)
Path("docker-compose.yml").write_text(text)
print(text, end="")
print("Wrote docker-compose.yml -> run: docker compose up -d --build")
