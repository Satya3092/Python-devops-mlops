"""
Day 047 — Reading Files: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
lines = words = chars = 0
with open("nginx_access.log", encoding="utf-8") as f:
    for line in f:
        lines += 1
        words += len(line.split())
        chars += len(line)
print(f"lines={lines} words={words} chars={chars}")

# ===== Task 2 =====
ips = set()
with open("nginx_access.log", encoding="utf-8") as f:
    for line in f:
        ips.add(line.split()[0])
print(sorted(ips))
print("Unique IPs:", len(ips))

# ===== Task 3 =====
stats = {}
total = errors = 0
with open("nginx_access.log", encoding="utf-8") as f:
    for line in f:
        parts = line.split()
        path, status = parts[5], int(parts[7])
        entry = stats.setdefault(path, {"requests": 0, "errors": 0})
        entry["requests"] += 1
        total += 1
        if status >= 400:
            entry["errors"] += 1
            errors += 1
print(f"{'PATH':<14}{'REQ':>4}{'ERR':>5}")
for path, s in sorted(stats.items(), key=lambda item: item[1]["requests"], reverse=True):
    print(f"{path:<14}{s['requests']:>4}{s['errors']:>5}")
print(f"Error rate: {errors / total * 100:.1f}%")
