"""
Day 024 — Tuples
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Tuple basics
# ======================================================================
database = ("db.internal", 5432, "orders")
print(database)
print("Host:", database[0])
print("Length:", len(database))

host, port, name = database
print(f"Connecting to {name} on {host}:{port}")

single = ("web",)
not_a_tuple = ("web")
print(type(single).__name__, type(not_a_tuple).__name__)

try:                                   # exceptions are covered on Day 52
    database[1] = 3306
except TypeError as error:
    print("Cannot modify a tuple:", error)

# ======================================================================
# Example 2 — Records, multiple return values and dictionary keys
# ======================================================================
# Each tuple is one fixed-format record
deployments = [
    ("orders", "2.1.0", "success"),
    ("payments", "1.4.2", "failed"),
    ("search", "3.0.1", "success"),
]
for service, version, result in deployments:
    print(f"{service:<10} {version:<7} {result}")

# A function returning two values gives back a tuple
def min_max(values):
    return min(values), max(values)

lowest, highest = min_max([120, 98, 450, 230])
print("Lowest:", lowest, "Highest:", highest)

# Tuples can be dict keys: latency per (region, service)
latency = {("us-east-1", "orders"): 120, ("eu-west-1", "orders"): 180}
print("EU orders latency:", latency[("eu-west-1", "orders")], "ms")

# Extended unpacking: first stage and the rest
first_stage, *other_stages = ("build", "test", "scan", "deploy")
print("First:", first_stage, "| Others:", other_stages)
