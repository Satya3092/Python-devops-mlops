"""
Day 071 — Automating Linux Commands with subprocess
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Pipelines and live output
# ======================================================================
import subprocess
import sys

# Pipeline: generate text -> sort -> uniq -c   (like: ... | sort | uniq -c)
generated = subprocess.run(["printf", "web\ndb\nweb\ncache\nweb\ndb\n"], capture_output=True, text=True, check=True)
sorted_text = subprocess.run(["sort"], input=generated.stdout, capture_output=True, text=True, check=True)
counted = subprocess.run(["uniq", "-c"], input=sorted_text.stdout, capture_output=True, text=True, check=True)
print("uniq -c result:")
print(counted.stdout.rstrip())

# The same counting done in Python (no extra processes needed)
counts = {}
for word in generated.stdout.split():
    counts[word] = counts.get(word, 0) + 1
print("Python result:", dict(sorted(counts.items())))

# Streaming output from a 'long-running' command
script = "import time\nfor i in range(1, 4):\n    print(f'step {i}/3 done', flush=True)\n    time.sleep(0.2)"
proc = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True)
for line in proc.stdout:
    print("[live]", line.rstrip())
print("exit code:", proc.wait())

# ======================================================================
# Example 2 — Parallel health checks with retries
# ======================================================================
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Simulated 'check' commands: each host is a small Python program that exits 0 (ok) or 1 (fail)
HOSTS = {"web-01": 0, "web-02": 0, "db-01": 1, "cache-01": 0, "queue-01": 0}


def check_host(host, attempts=2):
    """Run a (simulated) health check; retry once on failure."""
    exit_code = HOSTS[host]
    command = [sys.executable, "-c", f"import time, sys; time.sleep(0.5); sys.exit({exit_code})"]
    for attempt in range(1, attempts + 1):
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return host, "OK", attempt
    return host, "FAILED", attempts


start = time.perf_counter()
sequential = [check_host(h, attempts=1) for h in HOSTS]
sequential_time = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    parallel = list(pool.map(check_host, HOSTS))
parallel_time = time.perf_counter() - start

for host, status, attempts in parallel:
    print(f"{host:<9} {status:<7} after {attempts} attempt(s)")
print(f"Sequential took ~{sequential_time:.1f}s, parallel took ~{parallel_time:.1f}s")
failed = [h for h, s, _ in parallel if s != "OK"]
exit_code = 1 if failed else 0
print("Exit code for CI:", exit_code, "| failed:", failed)   # real script: sys.exit(exit_code)
