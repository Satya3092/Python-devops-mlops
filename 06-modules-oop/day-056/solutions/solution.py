"""
Day 056 — Modules and Imports: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import math
import subprocess
import sys

# ===== Task 1 =====
print(round(math.sqrt(2), 4))
print(math.floor(9.99))
print(math.factorial(5))

# ===== Task 2 =====
with open("string_tools.py", "w", encoding="utf-8") as f:
    f.write(
        "def slugify(text):\n"
        "    return '-'.join(text.lower().split())\n\n"
        "def shorten(text, n):\n"
        "    return text if len(text) <= n else text[:n] + '...'\n"
    )
import string_tools
print(string_tools.slugify("Payment Service API"))
print(string_tools.shorten("Deployment complete", 6))

# ===== Task 3 =====
with open("units.py", "w", encoding="utf-8") as f:
    f.write(
        "def bytes_to_human(n):\n"
        "    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:\n"
        "        if n < 1024:\n"
        "            return f'{n:.1f} {unit}'\n"
        "        n /= 1024\n"
        "    return f'{n:.1f} PB'\n\n"
        "if __name__ == '__main__':\n"
        "    print('self-test:', bytes_to_human(1536))\n"
    )
import units
for size in (512, 2048, 5_000_000, 7_500_000_000):
    print(size, "->", units.bytes_to_human(size))
result = subprocess.run([sys.executable, "units.py"], capture_output=True, text=True)
print(result.stdout.strip())
