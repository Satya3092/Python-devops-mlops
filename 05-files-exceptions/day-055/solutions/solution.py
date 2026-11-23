"""
Day 055 — File Processing Automation Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json
import os

LEVELS = ("INFO", "WARNING", "ERROR")

# ===== Task 1 =====
files = [(n, os.path.getsize(os.path.join("logs", n))) for n in os.listdir("logs") if n.endswith(".log")]
for name, size in sorted(files, key=lambda item: item[1], reverse=True):
    print(f"{name:<12}{size:>6} bytes")

# ===== Task 2 =====
with open("errors_only.log", "w", encoding="utf-8") as out:
    for name in sorted(os.listdir("logs")):
        if not name.endswith(".log"):
            continue
        with open(os.path.join("logs", name), encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) > 2 and parts[2] == "ERROR":
                    out.write(f"{name}: {line}")
with open("errors_only.log", encoding="utf-8") as f:
    print(f.read(), end="")

# ===== Task 3 =====
totals = {level: 0 for level in LEVELS}
bad_lines = 0
error_messages = {}
for name in sorted(os.listdir("logs")):
    if not name.endswith(".log"):
        continue
    with open(os.path.join("logs", name), encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            if len(parts) < 4 or parts[2] not in LEVELS:
                bad_lines += 1
                continue
            totals[parts[2]] += 1
            if parts[2] == "ERROR":
                message = " ".join(w for w in parts[3:] if "=" not in w)
                error_messages[message] = error_messages.get(message, 0) + 1
valid = sum(totals.values())
summary = {
    "totals": totals,
    "error_rate_percent": round(totals["ERROR"] / valid * 100, 1),
    "bad_lines": bad_lines,
    "top_error": max(error_messages, key=error_messages.get),
}
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
