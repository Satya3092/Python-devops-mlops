"""
Day 006 — Type Conversion: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
minutes = float(input("Timeout in minutes: "))
seconds = int(minutes * 60)
print()
print("Timeout:", seconds, "seconds")

# ===== Task 2 =====
debug_flag = "false"
workers = "4"
debug = debug_flag.lower() in ("true", "yes", "1")
worker_count = int(workers)
print(debug, type(debug))
print(worker_count, type(worker_count))
print("Wrong way bool('false') gives:", bool(debug_flag))

# ===== Task 3 =====
size_gb = float(input("File size (GB): "))
speed_mbps = float(input("Speed (Mbps): "))
seconds = size_gb * 8000 / speed_mbps
print()
print("Transfer time:", round(seconds / 60, 2), "minutes")
