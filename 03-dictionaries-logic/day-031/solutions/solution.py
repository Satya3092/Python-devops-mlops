"""
Day 031 — Range Function: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
print(list(range(2, 21, 2)))

# ===== Task 2 =====
ips = []
for host_part in range(1, 11):
    ips.append(f"192.168.1.{host_part}")
print(", ".join(ips))

# ===== Task 3 =====
minutes = list(range(3, 60, 7))
print("Minute marks:", minutes)
print("Runs per hour:", len(minutes))
print("Runs per day:", len(minutes) * 24)
for minute in minutes[:5]:
    print(f"00:{minute:02d}")
