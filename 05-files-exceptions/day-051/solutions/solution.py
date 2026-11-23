"""
Day 051 — Working with JSON: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json

# ===== Task 1 =====
me = {"name": "Satya", "skills": ["linux", "docker", "kubernetes"], "years": 10, "learning_python": True}
print(json.dumps(me, indent=2))

# ===== Task 2 =====
response = '{"pods": [{"name": "api-1", "status": "Running"}, {"name": "api-2", "status": "Pending"}, {"name": "db-0", "status": "Running"}]}'
pods = json.loads(response)["pods"]
running = [p["name"] for p in pods if p["status"] == "Running"]
print(running)
print("Not running:", len(pods) - len(running))

# ===== Task 3 =====
def load_flags(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_flags(path, flags):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(flags, f, indent=2)


def toggle(path, name):
    flags = load_flags(path)
    if name not in flags:
        raise KeyError(f"unknown flag: {name}")
    flags[name] = not flags[name]
    save_flags(path, flags)
    return flags[name]


save_flags("flags.json", {"dark_mode": False, "new_checkout": True, "beta_search": False})
print("dark_mode ->", toggle("flags.json", "dark_mode"))
print("new_checkout ->", toggle("flags.json", "new_checkout"))
with open("flags.json", encoding="utf-8") as f:
    print(f.read())
