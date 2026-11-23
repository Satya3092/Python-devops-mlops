"""
Day 057 — Python Packages: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from importlib import metadata

# ===== Task 1 =====
from infra_tools import hostname
for i in range(1, 4):
    print(hostname("api", "staging", i))

# ===== Task 2 =====
with open(os.path.join("infra_tools", "ports.py"), "w", encoding="utf-8") as f:
    f.write("def is_privileged(port):\n    return port < 1024\n")
from infra_tools.ports import is_privileged
print(22, is_privileged(22))
print(8080, is_privileged(8080))

# ===== Task 3 =====
def check_requirements(lines):
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, wanted = line.split("==")
        try:
            installed = metadata.version(name)
        except metadata.PackageNotFoundError:
            print(f"{name:<22} MISSING (wanted {wanted})")
            continue
        state = "OK" if installed == wanted else f"version mismatch (installed {installed})"
        print(f"{name:<22} {state}")


check_requirements(["# demo", "pip==0.0.1", "definitely-not-installed-pkg==1.0", ""])
