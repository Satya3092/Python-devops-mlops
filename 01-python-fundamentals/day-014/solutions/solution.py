"""
Day 014 — elif and Nested Conditions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
colour = input("Colour: ").strip().lower()
print()
if colour == "red":
    print("Stop")
elif colour == "yellow":
    print("Slow down")
elif colour == "green":
    print("Go")
else:
    print("Invalid colour")

# ===== Task 2 =====
status_code = 404
if 100 <= status_code < 200:
    print("Informational")
elif 200 <= status_code < 300:
    print("Success")
elif 300 <= status_code < 400:
    print("Redirection")
elif 400 <= status_code < 500:
    print("Client Error")
    if status_code == 401:
        print("Unauthorized: check your token")
    elif status_code == 403:
        print("Forbidden: check permissions")
    elif status_code == 404:
        print("Not Found: check the URL")
elif 500 <= status_code < 600:
    print("Server Error")
else:
    print("Unknown")

# ===== Task 3 =====
cpu = int(input("CPU %: "))
memory = int(input("Memory %: "))
disk = int(input("Disk %: "))
print()
if cpu >= 90 or memory >= 90 or disk >= 90:
    print("Status: CRITICAL")
    if disk >= 90:
        print("Suggested action: clean /var/log")
elif cpu >= 75 or memory >= 75 or disk >= 75:
    print("Status: WARNING")
else:
    print("Status: HEALTHY")
