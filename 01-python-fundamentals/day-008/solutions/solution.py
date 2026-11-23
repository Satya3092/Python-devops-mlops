"""
Day 008 — Comparison Operators: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
port = 22
print("Is SSH port:", port == 22)
print("Privileged port:", port < 1024)
print("Not HTTP:", port != 80)

# ===== Task 2 =====
print("'10' > '9' as strings:", "10" > "9")
print("10 > 9 as integers:", int("10") > int("9"))
print("Strings compare character by character, so '1' < '9' makes '10' smaller.")

# ===== Task 3 =====
uptime = 99.95
latency_ms = 215
error_rate = 0.4
uptime_ok = uptime >= 99.9
latency_ok = latency_ms < 200
errors_ok = error_rate <= 1
print("Uptime OK:", uptime_ok)
print("Latency OK:", latency_ok)
print("Error rate OK:", errors_ok)
print("SLA met:", uptime_ok and latency_ok and errors_ok)
