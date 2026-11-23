"""
Day 003 — Python Data Types: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
values = [8080, 99.9, "nginx", True, ["a", "b"], (1, 2), {"x", "y"}, {"k": "v"}, None]
for value in values:
    print(value, "->", type(value).__name__)

# ===== Task 2 =====
pod_name = "web-7d9f8"
replicas = 3
cpu_limit = 0.5
is_ready = True
ports = (80, 443)
labels = {"app": "web", "tier": "frontend"}
for item in [pod_name, replicas, cpu_limit, is_ready, ports, labels]:
    print(item, "->", type(item).__name__)

# ===== Task 3 =====
config = {"port": "8080", "debug": True, "workers": 4, "timeout": 2.5}
for key in ["port", "workers"]:
    value = config[key]
    if isinstance(value, int):
        print(key, "is valid (int)")
    else:
        print(key, "is INVALID: got", type(value).__name__, "but expected int")
