# DevOps Automation Snippets

[⬅ Resources](README.md)

```python
import os, sys, shutil, subprocess, logging, argparse, json
from pathlib import Path

# Environment & config
port = int(os.getenv("PORT", "8080"))
debug = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")

# Paths & files
base = Path(__file__).resolve().parent
for log in base.rglob("*.log"): print(log.name, log.stat().st_size)
shutil.make_archive("backup", "gztar", root_dir="data")

# Run commands safely
r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=10, check=False)
print(r.returncode, r.stdout)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger(__name__).warning("disk at %d%%", 91)

# CLI
p = argparse.ArgumentParser(); p.add_argument("--env", choices=["dev", "prod"], default="dev")
p.add_argument("--dry-run", action="store_true"); args = p.parse_args()

# HTTP
import requests
r = requests.get(url, params={"env": "prod"}, headers={"Authorization": f"Bearer {token}"}, timeout=5)
r.raise_for_status(); data = r.json()

# YAML
import yaml
config = yaml.safe_load(Path("config.yaml").read_text())

# AWS (credentials from SSO profile / IAM role - never in code)
import boto3
ec2 = boto3.client("ec2", region_name="ap-south-1")
for page in ec2.get_paginator("describe_instances").paginate(): ...

# Exit codes for CI/monitoring
sys.exit(0)  # 0 OK, 1 WARNING, 2 CRITICAL
```
