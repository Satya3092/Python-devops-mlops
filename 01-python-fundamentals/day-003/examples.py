"""
Day 003 — Python Data Types
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Inspecting types
# ======================================================================
port = 8080
cpu_load = 0.75
hostname = "web-01"
is_healthy = True
nothing_yet = None

print(port, type(port))
print(cpu_load, type(cpu_load))
print(hostname, type(hostname))
print(is_healthy, type(is_healthy))
print(nothing_yet, type(nothing_yet))

# ======================================================================
# Example 2 — One server described with every type
# ======================================================================
server = {                                   # dict: key -> value
    "name": "prod-web-01",                   # str
    "cpu_cores": 4,                          # int
    "load_average": 1.85,                    # float
    "in_maintenance": False,                 # bool
    "ports": (80, 443),                      # tuple (fixed)
    "tags": ["web", "nginx"],                # list (changeable)
    "environments": {"prod", "prod"},        # set (duplicates removed)
    "owner": None,                           # NoneType (unknown)
}

for key in server:                           # loop over keys (you'll learn loops on Day 29)
    value = server[key]
    print(key, "=", value, "->", type(value).__name__)

print("Is cpu_cores an int?", isinstance(server["cpu_cores"], int))
