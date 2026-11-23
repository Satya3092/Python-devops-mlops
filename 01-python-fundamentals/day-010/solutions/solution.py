"""
Day 010 — Assignment Operators: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
seconds = 10
seconds -= 3
print(seconds)
seconds -= 3
print(seconds)
seconds -= 3
print(seconds)

# ===== Task 2 =====
delay = 1
total_wait = 0
for attempt in range(1, 6):          # loops are covered on Day 29
    delay *= 2
    total_wait += delay
    print("Attempt", attempt, "-> wait", delay, "s")
print("Total waiting time:", total_wait, "s")

# ===== Task 3 =====
total_gb = 0
total_gb += 1.2
total_gb += 3.4
total_gb += 0.8
total_gb += 2.6
print("Total transferred:", round(total_gb, 2), "GB")
total_mb = total_gb
total_mb *= 1024
print("Total transferred:", round(total_mb, 1), "MB")
quota_gb = 10
quota_gb -= total_gb
print("Remaining quota:", round(quota_gb, 2), "GB")
