"""
Day 041 — Variable-Length Arguments (*args): reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def average(*values):
    if not values:
        return None
    return sum(values) / len(values)


print(average(4, 8, 15))
print(average(10))
print(average())

# ===== Task 2 =====
def build_path(*parts):
    cleaned = [part.strip("/") for part in parts if part.strip("/")]
    return "/" + "/".join(cleaned)


print(build_path("var", "/log/", "nginx"))
print(build_path("/etc/", "systemd", "system", "app.service"))

# ===== Task 3 =====
def health_summary(title, *statuses):
    print(f"== {title} ==")
    unhealthy = []
    for service, code in statuses:
        ok = 200 <= code < 300
        print(f"{service:<10}{code:>5}  {'healthy' if ok else 'UNHEALTHY'}")
        if not ok:
            unhealthy.append(service)
    print(f"Healthy: {len(statuses) - len(unhealthy)} | Unhealthy: {len(unhealthy)}")
    return unhealthy


checks = [("auth", 200), ("orders", 503), ("search", 200), ("payments", 500), ("cart", 204)]
print("Returned:", health_summary("Production health", *checks))
