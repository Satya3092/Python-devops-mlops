"""
Day 009 — Logical Operators: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
is_admin = False
is_developer = True
environment = "staging"
can_deploy = is_admin or (is_developer and environment != "prod")
print("Can deploy:", can_deploy)

# ===== Task 2 =====
hour = 14
is_weekday = True
safe_window = is_weekday and 10 <= hour <= 16
print("Safe window:", safe_window)
print("Freeze period:", not safe_window)

# ===== Task 3 =====
free_gb = 35
hour = 14
force_backup = True
backup_running = False
enough_space = free_gb > 20
night_time = 1 < hour < 5
allowed_time = night_time or force_backup
print("Enough space:", enough_space)
print("Night time:", night_time, "| Forced:", force_backup, "| Allowed time:", allowed_time)
print("No other backup running:", not backup_running)
print("Run backup:", enough_space and allowed_time and not backup_running)
