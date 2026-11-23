"""
Day 002 — Variables and Naming Conventions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Creating and updating variables
# ======================================================================
course = "100 Days of Python"
day = 2
is_learning = True

print(course)
print("Today is day", day)
print("Learning?", is_learning)

# Variables can be updated - the old value is replaced
day = 3
print("Tomorrow is day", day)

# ======================================================================
# Example 2 — Describing a server with variables
# ======================================================================
# Constants (UPPER_CASE) - settings we do not plan to change
MAX_CPU_PERCENT = 80
DEFAULT_PORT = 8080

# Variables (snake_case) describing one server
server_name = "prod-api-01"
environment = "production"
cpu_usage = 72
open_port = DEFAULT_PORT

# Multiple assignment in a single line
region, instance_type = "us-east-1", "t3.medium"

print("Server:", server_name)
print("Environment:", environment)
print("Region:", region, "| Type:", instance_type)
print("CPU usage:", cpu_usage, "% (limit", MAX_CPU_PERCENT, "%)")
print("Listening on port", open_port)
