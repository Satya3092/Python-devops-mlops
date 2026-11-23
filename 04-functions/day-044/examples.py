"""
Day 044 — Lambda Functions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Lambda basics
# ======================================================================
add = lambda a, b: a + b            # for demonstration only
print(add(2, 3))

numbers = [5, -3, 12, 0, -8, 7]
print("Doubled:", list(map(lambda n: n * 2, numbers)))
print("Positive:", list(filter(lambda n: n > 0, numbers)))
print("By absolute value:", sorted(numbers, key=lambda n: abs(n)))

# The same with comprehensions (often more readable)
print("Doubled:", [n * 2 for n in numbers])
print("Positive:", [n for n in numbers if n > 0])

words = ["kubernetes", "git", "docker", "ai"]
print("Shortest first:", sorted(words, key=len))
print("Longest:", max(words, key=lambda w: len(w)))

# ======================================================================
# Example 2 — Sorting and ranking infrastructure data
# ======================================================================
pods = [
    {"name": "api-7d9f", "restarts": 2, "cpu_m": 230, "age_h": 50},
    {"name": "worker-5c2a", "restarts": 14, "cpu_m": 480, "age_h": 3},
    {"name": "redis-0", "restarts": 0, "cpu_m": 90, "age_h": 400},
    {"name": "cron-28ab", "restarts": 5, "cpu_m": 15, "age_h": 1},
]

by_cpu = sorted(pods, key=lambda p: p["cpu_m"], reverse=True)
print("Top CPU consumers:", [p["name"] for p in by_cpu[:2]])

worst = max(pods, key=lambda p: p["restarts"])
print(f"Most restarts: {worst['name']} ({worst['restarts']})")

newest = min(pods, key=lambda p: p["age_h"])
print("Newest pod:", newest["name"])

# Multi-level sort: restarts descending, then name ascending
ranked = sorted(pods, key=lambda p: (-p["restarts"], p["name"]))
for p in ranked:
    print(f"{p['name']:<12} restarts={p['restarts']}")

# Version strings sorted numerically
releases = ["v1.10.0", "v1.2.3", "v1.9.12", "v2.0.0"]
print(sorted(releases, key=lambda v: [int(x) for x in v[1:].split(".")]))
