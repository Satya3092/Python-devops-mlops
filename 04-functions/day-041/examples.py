"""
Day 041 — Variable-Length Arguments (*args)
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Summing any number of values
# ======================================================================
def total(*numbers):
    print("Received:", numbers, type(numbers).__name__)
    return sum(numbers)


print(total(1, 2))
print(total(5, 10, 15, 20))
print(total())

values = [3, 6, 9]
print(total(*values))        # unpack the list

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)

# ======================================================================
# Example 2 — Running a command on many hosts
# ======================================================================
def run_on_hosts(command, *hosts, user="ubuntu"):
    """Simulate running a command on any number of hosts."""
    if not hosts:
        print("No hosts given - nothing to do")
        return []
    results = []
    for host in hosts:
        print(f"ssh {user}@{host} '{command}'")
        results.append((host, "ok"))
    return results


run_on_hosts("uptime")
run_on_hosts("df -h /", "web-01", "web-02")

web_tier = ["web-01", "web-02", "web-03"]
db_tier = ["db-01"]
results = run_on_hosts("sudo systemctl restart node_exporter", *web_tier, *db_tier, user="admin")
print("Results:", results)


def merge_tags(*tag_lists):
    """Merge any number of tag lists into one sorted unique list."""
    merged = set()
    for tags in tag_lists:
        merged.update(tags)
    return sorted(merged)


print(merge_tags(["web", "prod"], ["prod", "linux"], ["monitoring"]))
