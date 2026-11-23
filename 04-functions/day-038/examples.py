"""
Day 038 — Return Statement
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — print vs return
# ======================================================================
def add_print(a, b):
    print(a + b)            # shows the value but returns None


def add_return(a, b):
    return a + b            # gives the value back


x = add_print(2, 3)
y = add_return(2, 3)
print("x is", x)
print("y is", y)
print("y * 10 =", y * 10)


def min_max(numbers):
    return min(numbers), max(numbers)


low, high = min_max([7, 2, 9, 4])
print("Low:", low, "High:", high)

# ======================================================================
# Example 2 — Composable health-check functions
# ======================================================================
def percent(used, total):
    """Return usage as a percentage, or 0.0 when total is zero."""
    if total == 0:
        return 0.0                      # early return (guard clause)
    return used / total * 100


def classify(value, warning=75, critical=90):
    """Return OK / WARNING / CRITICAL for a percentage."""
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


def check_server(name, mem_used, mem_total, disk_used, disk_total):
    """Return a dict with the results so other code can use them."""
    mem_pct = percent(mem_used, mem_total)
    disk_pct = percent(disk_used, disk_total)
    return {
        "name": name,
        "memory": (round(mem_pct, 1), classify(mem_pct)),
        "disk": (round(disk_pct, 1), classify(disk_pct)),
    }


results = [
    check_server("web-01", 6.2, 8, 40, 100),
    check_server("db-01", 30, 32, 410, 500),
    check_server("new-vm", 0, 0, 1, 50),
]
for r in results:
    print(f"{r['name']:<7} memory={r['memory']} disk={r['disk']}")

critical_servers = [r["name"] for r in results if "CRITICAL" in (r["memory"][1], r["disk"][1])]
print("Critical servers:", critical_servers)
