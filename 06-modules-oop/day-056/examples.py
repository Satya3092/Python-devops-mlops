"""
Day 056 — Modules and Imports
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Using the standard library
# ======================================================================
import math
import random
from datetime import date, timedelta
import platform as pf

print("sqrt(144) =", math.sqrt(144))
print("ceil(7.2) =", math.ceil(7.2))
print("pi =", round(math.pi, 4))

random.seed(42)                     # fixed seed -> same "random" numbers every run
print("Random port:", random.randint(30000, 32767))
print("Random choice:", random.choice(["web-01", "web-02", "web-03"]))

release = date(2026, 11, 20)
print("Release date + 14 days:", release + timedelta(days=14))
print("Running on:", pf.system())

# ======================================================================
# Example 2 — Importing your own module
# ======================================================================
import devops_utils
from devops_utils import percent, status

print("Module name:", devops_utils.__name__)
print("Default threshold:", devops_utils.DEFAULT_THRESHOLD)

disks = {"/": (41, 50), "/var": (19, 20), "/data": (120, 500)}
for mount, (used, total) in disks.items():
    usage = percent(used, total)
    print(f"{mount:<6} {usage:>5}% {status(usage)}")

print("Docstring:", percent.__doc__)
