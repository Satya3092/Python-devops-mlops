"""
Day 012 — Conditional Statements (if)
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — A simple if
# ======================================================================
temperature = 35

if temperature > 30:
    print("It is hot today.")
    print("Remember to drink water.")

print("This line always runs.")

# ======================================================================
# Example 2 — Disk usage alerts
# ======================================================================
disk_usage = int(input("Disk usage %: "))
log_files = ["app.log", "error.log"]
maintenance_message = ""

if disk_usage >= 80:
    print("WARNING: disk usage is", disk_usage, "%")

if disk_usage >= 95:
    print("CRITICAL: clean up immediately!")

if log_files:                      # a non-empty list is truthy
    print("Log files to rotate:", log_files)

if not maintenance_message:        # empty string is falsy
    print("No maintenance message set.")

print("Check complete.")
