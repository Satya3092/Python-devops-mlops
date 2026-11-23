"""
Day 017 — String Indexing
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Reading characters by position
# ======================================================================
tool = "kubernetes"
print("First:", tool[0])
print("Second:", tool[1])
print("Last:", tool[-1])
print("Second last:", tool[-2])
print("Length:", len(tool), "-> last index is", len(tool) - 1)
print("Same last char:", tool[len(tool) - 1])

# ======================================================================
# Example 2 — Decoding instance naming conventions
# ======================================================================
# Naming convention: <env-letter><region-digit>-<role>
# e.g. "p1-web" = production, region 1, web server
instance_name = "p1-web"

env_code = instance_name[0]
region_code = instance_name[1]
last_char = instance_name[-1]

if env_code == "p":
    environment = "production"
elif env_code == "s":
    environment = "staging"
else:
    environment = "development"

print("Instance:", instance_name)
print("Environment:", environment)
print("Region number:", region_code)
print("Ends with:", last_char)

# File permission string from 'ls -l'
permissions = "-rwxr-x---"
print("Is a directory?", permissions[0] == "d")
print("Owner can execute?", permissions[3] == "x")
print("Others can read?", permissions[7] == "r")
