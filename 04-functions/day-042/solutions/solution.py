"""
Day 042 — Variable-Length Arguments (**kwargs): reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def print_settings(**settings):
    for key in sorted(settings):
        print(f"{key.upper()} = {settings[key]}")


print_settings(timeout=30, debug=False, log_level="INFO")

# ===== Task 2 =====
def connection_string(driver, **params):
    host = params.get("host", "localhost")
    port = params.get("port", 5432)
    return f"{driver}://{params['user']}:{params['password']}@{host}:{port}/{params['db']}"


db_config = {"user": "app", "password": "secret", "host": "db.internal", "db": "orders"}
print(connection_string("postgresql", **db_config))

# ===== Task 3 =====
def kubectl_get(resource, *names, namespace="default", **labels):
    parts = ["kubectl get", resource, *names, f"-n {namespace}"]
    if labels:
        selector = ",".join(f"{k}={v}" for k, v in labels.items())
        parts.append(f"-l {selector}")
    return " ".join(parts)


print(kubectl_get("pods"))
print(kubectl_get("pods", namespace="prod", app="orders", tier="backend"))
print(kubectl_get("deployment", "api", "worker", namespace="jobs"))
