"""
Day 099 — Dockerizing an ML Application
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Lint the Dockerfile with Python (a mini hadolint)
# ======================================================================
from pathlib import Path

RULES = [
    ("pinned base image (no :latest)", lambda t: "FROM" in t and ":latest" not in t),
    ("slim or minimal base", lambda t: "-slim" in t or "alpine" in t or "distroless" in t),
    ("multi-stage build", lambda t: t.count("FROM ") >= 2),
    ("requirements copied before source (layer caching)",
     lambda t: t.index("COPY requirements.txt") < t.index("COPY app.py")),
    ("pip cache disabled", lambda t: "PIP_NO_CACHE_DIR=1" in t or "--no-cache-dir" in t),
    ("runs as non-root USER", lambda t: "\nUSER " in t and "USER root" not in t),
    ("HEALTHCHECK defined", lambda t: "HEALTHCHECK" in t),
    ("exec-form CMD", lambda t: 'CMD ["' in t),
    ("no secrets in ENV", lambda t: not any(w in t.upper() for w in ("PASSWORD=", "SECRET=", "AWS_SECRET"))),
]

dockerfile = Path("Dockerfile").read_text()
passed = 0
for name, check in RULES:
    ok = check(dockerfile)
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
print(f"{passed}/{len(RULES)} checks passed")

ignored = [line.strip() for line in Path(".dockerignore").read_text().splitlines()
           if line.strip() and not line.startswith("#")]
print(".dockerignore excludes:", ignored)
print("Stages:", [line.split(" AS ")[1] for line in dockerfile.splitlines() if line.startswith("FROM ")])

# ======================================================================
# Example 2 — Build, run and smoke-test the container from Python
# ======================================================================
import shutil
import subprocess
import sys
import time

IMAGE, NAME, PORT = "server-failure-api:1.0.0", "sfa-demo", "8000"


def sh(*cmd, check=True):
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(result.stderr.strip())
    return result.stdout.strip()


if not shutil.which("docker"):
    sys.exit("Docker is not installed - see https://docs.docker.com/get-docker/")

sh("docker", "build", "-t", IMAGE, ".")
print(sh("docker", "image", "ls", IMAGE, "--format", "{{.Repository}}:{{.Tag}} {{.Size}}"))
sh("docker", "rm", "-f", NAME, check=False)
sh("docker", "run", "-d", "--name", NAME, "-p", f"{PORT}:8000", IMAGE)

for _ in range(30):                                   # wait for the HEALTHCHECK
    status = sh("docker", "inspect", "--format", "{{.State.Health.Status}}", NAME)
    if status == "healthy":
        break
    time.sleep(2)
print("container health:", status)
print("user inside container:", sh("docker", "exec", NAME, "whoami"))

smoke = subprocess.run([sys.executable, "smoke_test.py"], env={"BASE_URL": f"http://127.0.0.1:{PORT}", "PATH": ""},
                       capture_output=True, text=True)
print(smoke.stdout.strip())
print("last log line:", sh("docker", "logs", NAME).splitlines()[-1][-60:])
sh("docker", "rm", "-f", NAME)
print("smoke test exit code:", smoke.returncode)
