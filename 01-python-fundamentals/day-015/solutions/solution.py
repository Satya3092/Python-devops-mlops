"""
Day 015 — Python Fundamentals Revision and Mini Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
size_mb = float(input("Size in MB: "))
print()
print("Size in GB:", round(size_mb / 1024, 2))
print("Size in bytes:", int(size_mb * 1024 * 1024))
if size_mb > 1024:
    print("Large file")

# ===== Task 2 =====
username = input("Username: ").strip()
age = int(input("Age: "))
print()
if username == "":
    print("Access denied: empty username")
elif not 18 <= age <= 65:
    print("Access denied: age out of range")
else:
    print("Access granted")

# ===== Task 3 =====
WARNING_LEVEL, CRITICAL_LEVEL = 75, 90
name = input("Server: ")
cpu = float(input("CPU %: "))
disk_total = float(input("Disk total GB: "))
disk_used = float(input("Disk used GB: "))
load_average = float(input("Load average: "))
cores = int(input("CPU cores: "))
print()
disk_percent = disk_used / disk_total * 100
load_per_core = load_average / cores

statuses = []
for value in (cpu, disk_percent):
    if value >= CRITICAL_LEVEL:
        statuses.append("CRITICAL")
    elif value >= WARNING_LEVEL:
        statuses.append("WARNING")
    else:
        statuses.append("OK")

if load_per_core > 2.0:
    load_status = "CRITICAL"
elif load_per_core > 1.0:
    load_status = "WARNING"
else:
    load_status = "OK"
statuses.append(load_status)

overall = "CRITICAL" if "CRITICAL" in statuses else "WARNING" if "WARNING" in statuses else "OK"
print("Server:", name)
print("CPU:", cpu, "% ->", statuses[0])
print("Disk:", round(disk_percent, 1), "% ->", statuses[1], "| free:", disk_total - disk_used, "GB")
print("Load per core:", round(load_per_core, 2), "->", load_status)
print("Overall:", overall)
