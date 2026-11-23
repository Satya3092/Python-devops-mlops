"""
Day 046 — File Handling Introduction: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os

# ===== Task 1 =====
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello from Python!\n")
with open("hello.txt", "r", encoding="utf-8") as f:
    print(f.read().strip())

# ===== Task 2 =====
if not os.path.exists("config.ini"):
    with open("config.ini", "w", encoding="utf-8") as f:
        f.write("[app]\ndebug=false\n")
with open("config.ini", encoding="utf-8") as f:
    print(f.read().strip())
print("Size:", os.path.getsize("config.ini"), "bytes")

# ===== Task 3 =====
hosts = ["web-01", "web-02", "web-03", "db-01", "cache-01"]
with open("servers.txt", "w", encoding="utf-8") as f:
    for host in hosts:
        f.write(host + "\n")
count = 0
with open("servers.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.strip())
        count += 1
print("Total:", count)
