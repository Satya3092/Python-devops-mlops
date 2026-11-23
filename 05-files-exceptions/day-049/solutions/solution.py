"""
Day 049 — Append Mode: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os

# ===== Task 1 =====
with open("shopping.txt", "a", encoding="utf-8") as f:
    f.write("milk\n")
    f.write("bread\n")
with open("shopping.txt", "a", encoding="utf-8") as f:
    f.write("coffee\n")
with open("shopping.txt", encoding="utf-8") as f:
    print(f.read(), end="")

# ===== Task 2 =====
def audit(user, action):
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(f"{user}|{action}\n")


audit("asha", "deploy orders-api")
audit("ravi", "restart redis")
audit("asha", "scale worker to 5")
audit("asha", "rollback payments")
counts = {}
with open("audit.log", encoding="utf-8") as f:
    for line in f:
        user = line.split("|")[0]
        counts[user] = counts.get(user, 0) + 1
print(counts)

# ===== Task 3 =====
statuses = [200, 200, 503, 200, 500, 200]
for number, status in enumerate(statuses, start=1):
    new_file = not os.path.exists("uptime.csv")
    with open("uptime.csv", "a", encoding="utf-8") as f:
        if new_file:
            f.write("check,status,state\n")
        state = "UP" if status == 200 else "DOWN"
        f.write(f"{number},{status},{state}\n")
up = total = 0
with open("uptime.csv", encoding="utf-8") as f:
    next(f)                      # skip header
    for line in f:
        total += 1
        if line.strip().endswith("UP"):
            up += 1
print(f"Availability: {up / total * 100:.1f}%")
