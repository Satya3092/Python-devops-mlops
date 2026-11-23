"""
Day 098 — Building an ML API using FastAPI: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import subprocess
import sys
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# ===== Task 1 =====
class Deployment(BaseModel):
    service: str = Field(..., min_length=3)
    replicas: int = Field(..., ge=1, le=50)
    env: Literal["dev", "staging", "prod"]


print(Deployment(service="orders", replicas=3, env="prod"))
try:
    Deployment(service="ab", replicas=0, env="qa")
except ValidationError as error:
    for e in error.errors():
        print(e["loc"][0], "->", e["msg"])

# ===== Task 2 =====
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

demo = FastAPI()
SERVERS = {"web-01": "prod", "batch-01": "dev"}


@demo.get("/ping")
def ping():
    return {"pong": True}


@demo.get("/servers/{name}")
def get_server(name: str):
    if name not in SERVERS:
        raise HTTPException(status_code=404, detail=f"server {name} not found")
    return {"name": name, "env": SERVERS[name]}


@demo.get("/servers")
def list_servers(env: str | None = None):
    return [n for n, e in SERVERS.items() if env is None or e == env]


client = TestClient(demo)
print("GET  /ping            ->", client.get("/ping").json())
print("GET  /servers/web-01  ->", client.get("/servers/web-01").json())
r = client.get("/servers/nope")
print("GET  /servers/nope    ->", r.status_code, r.json())
print("GET  /servers?env=dev ->", client.get("/servers", params={"env": "dev"}).json())

# ===== Task 3 =====
subprocess.run([sys.executable, "train.py"], capture_output=True, check=True)
result = subprocess.run([sys.executable, "-m", "pytest", "-q", "test_app.py"], capture_output=True, text=True)
print(result.stdout.strip().splitlines()[-1].split(" in ")[0])
