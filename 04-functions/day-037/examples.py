"""
Day 037 — Function Parameters and Arguments
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Functions with parameters
# ======================================================================
def greet(name):
    print(f"Hello, {name}!")


def add(a, b):
    print(f"{a} + {b} = {a + b}")


def describe_pet(animal, name):
    print(f"I have a {animal} called {name}.")


greet("Asha")
greet("Ravi")
add(3, 4)
add(10, -2)
describe_pet("dog", "Bruno")
describe_pet("Bruno", "dog")      # wrong order -> wrong meaning!

# ======================================================================
# Example 2 — Reusable checks for many servers
# ======================================================================
def check_threshold(server, metric, value, limit):
    """Print an OK/ALERT line for one metric of one server."""
    status = "ALERT" if value > limit else "OK"
    print(f"{server:<8} {metric:<6} {value:>5.1f}% (limit {limit}%) -> {status}")


def tag_instance(tags, key, value):
    """Add a tag to a tags dictionary (modifies the dict in place)."""
    tags[key] = value


check_threshold("web-01", "cpu", 72.5, 80)
check_threshold("web-01", "disk", 91.0, 85)
check_threshold("db-01", "memory", 88.4, 90)

instance_tags = {"Name": "web-01"}
tag_instance(instance_tags, "Env", "prod")
tag_instance(instance_tags, "Owner", "team-web")
print("Tags after function calls:", instance_tags)
