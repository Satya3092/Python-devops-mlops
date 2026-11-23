"""
Day 029 — For Loops: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")

# ===== Task 2 =====
services = ["auth", "orders", "search"]
ports = [8001, 8002, 8003]
for number, (service, port) in enumerate(zip(services, ports), start=1):
    print(f"{number}. http://{service}.internal:{port}/health")

# ===== Task 3 =====
files = [("app.log", 120, 2), ("app.log.1", 300, 10), ("backup.tar", 4096, 40), ("core.dump", 2048, 15), ("notes.txt", 1, 100)]
total_mb = 0
for name, size_mb, days_old in files:
    if days_old > 7 and size_mb > 100:
        print(f"Candidate: {name} ({size_mb} MB, {days_old} days old)")
        total_mb += size_mb
print(f"Space to free: {total_mb / 1024:.2f} GB")
