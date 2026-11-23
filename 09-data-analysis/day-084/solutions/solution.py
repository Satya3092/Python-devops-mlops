"""
Day 084 — NumPy Introduction: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import numpy as np

# ===== Task 1 =====
for arr in (np.arange(1, 11), np.zeros((3, 3)), np.linspace(0, 100, 5)):
    print(arr.tolist(), arr.shape, arr.dtype)

# ===== Task 2 =====
sizes = np.array([1073741824, 536870912, 2147483648, 268435456])
gb = sizes / 1024 ** 3
print(gb.tolist(), "total:", gb.sum(), "GB")

# ===== Task 3 =====
rng = np.random.default_rng(1)
requests_per_hour = rng.integers(1000, 5001, size=24)
print(requests_per_hour)
print("Busiest hour:", int(requests_per_hour.argmax()), "with", int(requests_per_hour.max()))
print("Quietest hour:", int(requests_per_hour.argmin()), "with", int(requests_per_hour.min()))
print("Hours over 4000:", int((requests_per_hour > 4000).sum()))
