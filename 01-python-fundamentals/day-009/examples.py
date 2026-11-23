"""
Day 009 — Logical Operators
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Truth table in code
# ======================================================================
print("True and False =", True and False)
print("True or False  =", True or False)
print("not True       =", not True)

is_weekend = False
is_holiday = True
print("Day off?", is_weekend or is_holiday)

print("Empty list is falsy:", not [])
print("'' or 'default' ->", "" or "default")

# ======================================================================
# Example 2 — Deciding when to page the on-call engineer
# ======================================================================
environment = "prod"
cpu_usage = 92
error_rate = 0.5
in_maintenance_window = False

high_cpu = cpu_usage > 90
high_errors = error_rate > 5
is_production = environment == "prod"

# Page only for production, outside maintenance, if something is wrong
should_page = is_production and not in_maintenance_window and (high_cpu or high_errors)
print("High CPU:", high_cpu, "| High errors:", high_errors)
print("Page on-call engineer?", should_page)

# Safe defaults with 'or'
configured_region = ""
region = configured_region or "us-east-1"
print("Region used:", region)
