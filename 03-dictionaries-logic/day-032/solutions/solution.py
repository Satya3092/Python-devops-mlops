"""
Day 032 — Break, Continue, and Pass: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
for number in [4, 7, 2, -1, 9]:
    if number < 0:
        print("Stopped at", number)
        break
    print(number)

# ===== Task 2 =====
hosts = ["web-01", "web-02 (maintenance)", "web-03", "db-01 (maintenance)"]
skipped = 0
for host in hosts:
    if "(maintenance)" in host:
        skipped += 1
        continue
    print("Deploying to", host)
print("Skipped:", skipped)

# ===== Task 3 =====
test_cases = [
    [("replica-1", 503), ("replica-2", 500), ("replica-3", 200), ("replica-4", 200)],
    [("replica-1", 500), ("replica-2", 500)],
]
for replicas in test_cases:
    for name, status in replicas:
        if status == 200:
            print("Routing traffic to", name)
            break
    else:
        print("All replicas down - failing over to DR region")
