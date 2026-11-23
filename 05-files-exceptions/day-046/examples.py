"""
Day 046 — File Handling Introduction
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Reading a file with `with`
# ======================================================================
import os

filename = "welcome.txt"
print("Exists?", os.path.exists(filename))

with open(filename, "r", encoding="utf-8") as file:
    content = file.read()
    print("Inside with - closed?", file.closed)

print("Outside with - closed?", file.closed)
print("Content:")
print(content)
print("Characters:", len(content))

# ======================================================================
# Example 2 — Writing a small status file and reading it back
# ======================================================================
import os

status_file = "deploy_status.txt"

with open(status_file, "w", encoding="utf-8") as file:
    file.write("service=orders-api\n")
    file.write("version=2.4.1\n")
    file.write("status=success\n")

print("File size:", os.path.getsize(status_file), "bytes")

with open(status_file, "r", encoding="utf-8") as file:
    for line in file:
        key, value = line.strip().split("=")
        print(f"{key:<8}: {value}")

if os.path.exists("missing.txt"):
    print("missing.txt found")
else:
    print("missing.txt does not exist - skipping")
