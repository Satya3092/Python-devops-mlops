"""
Day 061 — Subprocess Module
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Running commands and reading results
# ======================================================================
import subprocess
import sys

result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
print("Return code:", result.returncode)
print("Output:", result.stdout.strip() or result.stderr.strip())

result = subprocess.run(["echo", "Hello from a child process"], capture_output=True, text=True)
print("echo said:", result.stdout.strip())

result = subprocess.run(["ls", "this-folder-does-not-exist"], capture_output=True, text=True)
print("ls exit code:", result.returncode)
print("ls stderr:", result.stderr.strip().split(":")[-1].strip())

try:
    subprocess.run(["ls", "this-folder-does-not-exist"], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as error:
    print("CalledProcessError, exit code", error.returncode)

try:
    subprocess.run(["sleep", "5"], timeout=1)
except subprocess.TimeoutExpired:
    print("Command timed out after 1 second")

# ======================================================================
# Example 2 — A safe command runner for automation
# ======================================================================
import shutil
import subprocess


def run(command, timeout=30):
    """Run a command list, return (ok, output). Never raises for normal failures."""
    if shutil.which(command[0]) is None:
        return False, f"{command[0]}: command not found"
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    output = (result.stdout or result.stderr).strip()
    return result.returncode == 0, output


checks = {
    "Kernel": ["uname", "-sr"],
    "Disk (/)": ["df", "-h", "/"],
    "Uptime": ["uptime"],
    "Docker": ["docker", "--version"],
    "Bad command": ["kubectl-that-does-not-exist", "version"],
}

for name, command in checks.items():
    ok, output = run(command)
    first_line = output.splitlines()[-1] if output else ""
    print(f"[{'OK' if ok else 'FAIL':<4}] {name:<12} {first_line[:60]}")

# Processing output in Python instead of using shell pipes
ok, output = run(["df", "-P"])
if ok:
    rows = [line.split() for line in output.splitlines()[1:]]
    busiest = max(rows, key=lambda r: int(r[4].rstrip("%")))
    print(f"Fullest filesystem: {busiest[5]} at {busiest[4]}")
