"""
Day 044 — Lambda Functions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
students = [("Asha", 88), ("Ravi", 72), ("Meera", 95)]
print(sorted(students, key=lambda s: s[1], reverse=True))

# ===== Task 2 =====
files = ["app.log", "data.csv", "error.log", "model.pkl", "access.log"]
log_files = filter(lambda name: name.endswith(".log"), files)
print(list(map(lambda name: name.upper(), log_files)))

# ===== Task 3 =====
instances = [("i-1", "m5.xlarge", 0.192, 8), ("i-2", "t3.micro", 0.0104, 55),
             ("i-3", "c5.2xlarge", 0.34, 12), ("i-4", "m5.large", 0.096, 71)]
idle = filter(lambda i: i[3] < 15, instances)
ranked = sorted(idle, key=lambda i: i[2] * 730, reverse=True)
savings = 0
for instance_id, instance_type, hourly, cpu in ranked:
    monthly = hourly * 730
    savings += monthly
    print(f"{instance_id} {instance_type:<11} cpu={cpu}% monthly=${monthly:.2f}")
print(f"Potential monthly savings: ${savings:.2f}")
