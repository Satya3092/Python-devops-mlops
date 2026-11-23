"""
Day 012 — Conditional Statements (if): reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
number = int(input("Number: "))
print()
if number > 0:
    print("Positive")

# ===== Task 2 =====
password = input("Password: ")
print()
if len(password) < 8:
    print("Warning: password is shorter than 8 characters")
if password == "password":
    print("Warning: never use 'password' as a password")

# ===== Task 3 =====
restart_count = 6
exit_code = 137
status = "CrashLoopBackOff"
if restart_count > 5:
    print("Warning: container restarted", restart_count, "times")
if exit_code == 137:
    print("Killed by OOM (exit code 137) - increase memory limit")
if status == "CrashLoopBackOff":
    print("Pod is crash looping")
