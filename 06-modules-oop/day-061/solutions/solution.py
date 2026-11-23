"""
Day 061 — Subprocess Module: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import shutil
import subprocess
import sys

# ===== Task 1 =====
result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
print((result.stdout or result.stderr).split()[1])

# ===== Task 2 =====
def git_info():
    if not shutil.which("git"):
        return {"git": "not installed"}
    result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
    return {"git": result.stdout.split()[-1]}


print(git_info())

# ===== Task 3 =====
def count_lines(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    return len(result.stdout.splitlines())


def top_processes(n):
    try:
        result = subprocess.run(["ps", "-eo", "pid,comm,%mem", "--sort=-%mem"],
                                capture_output=True, text=True, timeout=10, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print("Could not list processes:", error)
        return []
    rows = []
    for line in result.stdout.splitlines()[1:n + 1]:
        pid, name, mem = line.split()
        rows.append((int(pid), name, float(mem)))
    return rows


print("Lines printed by 'ps -e':", count_lines(["ps", "-e"]) > 0)
print(f"{'PID':>7}  {'NAME':<16}{'%MEM':>6}")
for pid, name, mem in top_processes(3):
    print(f"{pid:>7}  {name:<16}{mem:>6.1f}")
