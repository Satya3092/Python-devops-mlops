"""
Day 071 — Automating Linux Commands with subprocess: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# ===== Task 1 =====
words = "\n".join("apple banana apple cherry banana apple".split()) + "\n"
step1 = subprocess.run(["sort"], input=words, capture_output=True, text=True, check=True)
step2 = subprocess.run(["uniq", "-c"], input=step1.stdout, capture_output=True, text=True, check=True)
step3 = subprocess.run(["sort", "-rn"], input=step2.stdout, capture_output=True, text=True, check=True)
for line in step3.stdout.splitlines():
    count, word = line.split()
    print(word, count)

# ===== Task 2 =====
child = "for n in range(1, 5):\n    print(f'Downloading part {n}', flush=True)"
proc = subprocess.Popen([sys.executable, "-c", child], stdout=subprocess.PIPE, text=True)
for k, line in enumerate(proc.stdout, start=1):
    print(f"[{k}] {line.rstrip()}")
print("exit code:", proc.wait())

# ===== Task 3 =====
def run_one(item):
    name, command = item
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    except FileNotFoundError:
        return name, (127, "command not found")
    output = (result.stdout or result.stderr).strip().splitlines()
    return name, (result.returncode, output[0] if output else "")


def run_all(commands, workers=3):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return dict(pool.map(run_one, commands.items()))


commands = {
    "kernel": ["uname", "-s"],
    "python": [sys.executable, "--version"],
    "missing": ["ls", "/nonexistent"],
    "echo": ["echo", "done"],
}
results = run_all(commands)
failures = 0
for name in sorted(results):
    code, first = results[name]
    failures += code != 0
    print(f"{name:<8} rc={code:<3} {first.split(':')[0] if code else first}")
print("Failures:", failures)
