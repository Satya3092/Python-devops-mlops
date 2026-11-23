"""
Day 016 — Strings Introduction: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
service = "auth"
env = "prod"
number = "03"
hostname = service + "-" + env + "-" + number
print(hostname)
print("Length:", len(hostname))

# ===== Task 2 =====
log_line = "2026-11-20 10:21:01 WARNING Disk usage 91% on /var"
for word in ["ERROR", "WARNING", "Disk", "disk"]:
    print(word, "present:", word in log_line)

# ===== Task 3 =====
message = "Deployment v2.3.0 complete"
width = len(message) + 4
print("#" * width)
print("# " + message + " #")
print("#" * width)
