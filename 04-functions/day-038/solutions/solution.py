"""
Day 038 — Return Statement: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


for c in (0, 37, 100):
    print(c, "C =", round(to_fahrenheit(c), 1), "F")

# ===== Task 2 =====
def is_valid_port(port):
    return isinstance(port, int) and 1 <= port <= 65535


for p in (22, 0, 70000, 8080):
    print(p, is_valid_port(p))

# ===== Task 3 =====
def parse_log_line(line):
    parts = line.split(" ", 3)
    if len(parts) < 4:
        return None
    date, time, level, message = parts
    return date, time, level, message


lines = [
    "2026-11-20 10:15:32 ERROR Database timeout",
    "2026-11-20 10:15:40 INFO Retry succeeded",
    "corrupted line",
    "2026-11-20 10:16:02 ERROR Disk full",
]
counts = {}
for line in lines:
    parsed = parse_log_line(line)
    if parsed is None:
        print("Skipped invalid line:", line)
        continue
    print(parsed)
    level = parsed[2]
    counts[level] = counts.get(level, 0) + 1
print(counts)
