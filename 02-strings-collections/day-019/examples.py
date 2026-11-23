"""
Day 019 — String Methods
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Everyday string methods
# ======================================================================
raw = "   Production-Server  \n"
print(repr(raw))
clean = raw.strip()
print(repr(clean))
print(clean.lower())
print(clean.upper())
print(clean.replace("Server", "DB"))
print(clean.startswith("Prod"), clean.endswith(".log"))
print("Position of '-':", clean.find("-"))
print("Count of 'o':", clean.count("o"))
print("8080".isdigit(), "80a".isdigit())

# ======================================================================
# Example 2 — Parsing command output and environment data
# ======================================================================
# Output of 'df -h' for one filesystem
df_line = "/dev/sda1        50G   41G  9.0G  82% /"
fields = df_line.split()
print("Fields:", fields)
filesystem, size, used, available, use_percent, mount = fields
print("Mount", mount, "is", use_percent, "full")
usage = int(use_percent.rstrip("%"))
if usage > 80:
    print("Warning: high disk usage on", filesystem)

# Comma-separated host list from an environment variable
hosts_env = " web-01, web-02 ,web-03 "
hosts = [h.strip() for h in hosts_env.split(",")]   # list comprehension, Day 34
print("Hosts:", hosts)
print("Ansible inventory line:", " ".join(hosts))

# Normalise user input
answer = "  YES "
print("Confirmed?", answer.strip().lower() == "yes")

# Build a Kubernetes-style label from a title
title = "Payment Service API"
print("Label:", title.lower().replace(" ", "-"))
