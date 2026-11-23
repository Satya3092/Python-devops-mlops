"""
Day 026 — Dictionaries: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
book = {"title": "The Phoenix Project", "author": "Gene Kim", "year": 2013}
print("Title:", book["title"])
print("Author:", book["author"])
print("Year:", book["year"])
book["rating"] = 5
book["year"] = 2018
print(book)

# ===== Task 2 =====
ports = {"ssh": 22, "http": 80, "https": 443, "postgres": 5432, "redis": 6379}
print("postgres:", ports["postgres"])
print("mongodb:", ports.get("mongodb", "unknown"))
print("Known services:", len(ports))

# ===== Task 3 =====
defaults = {"replicas": 1, "log_level": "INFO", "debug": False}
prod_overrides = {"replicas": 5, "log_level": "WARNING"}
final_config = defaults.copy()
overridden = []
for key in prod_overrides:
    final_config[key] = prod_overrides[key]
    overridden.append(key)
print("Final config:", final_config)
print("Overridden keys:", overridden)
