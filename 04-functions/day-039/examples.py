"""
Day 039 — Default Arguments
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Defaults in action
# ======================================================================
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"


print(greet("Asha"))
print(greet("Ravi", "Good morning"))
print(greet("Meera", "Hi", "?"))


# The mutable default trap
def add_item_buggy(item, items=[]):
    items.append(item)
    return items


print(add_item_buggy("a"))
print(add_item_buggy("b"))       # surprise: 'a' is still there!


def add_item_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item_safe("a"))
print(add_item_safe("b"))

# ======================================================================
# Example 2 — A docker run command builder with sensible defaults
# ======================================================================
def docker_run(image, tag="latest", name=None, ports=None, detach=True, restart="unless-stopped"):
    """Build a docker run command; only the image is required."""
    parts = ["docker run"]
    if detach:
        parts.append("-d")
    if name:
        parts.append(f"--name {name}")
    for host_port, container_port in (ports or {}).items():
        parts.append(f"-p {host_port}:{container_port}")
    parts.append(f"--restart {restart}")
    parts.append(f"{image}:{tag}")
    return " ".join(parts)


print(docker_run("redis"))
print(docker_run("nginx", "1.27", name="web", ports={8080: 80}))
print(docker_run("python", "3.12", detach=False, restart="no"))
