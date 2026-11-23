"""
Day 023 — List Methods: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
history = []
history.append("mkdir app")
history.append("cd app")
history.append("git init")
print("Undo:", history.pop())
print("Undo:", history.pop())
print("Remaining:", history)

# ===== Task 2 =====
team_a = ["nginx", "redis"]
team_b = ["redis", "postgres", "nginx", "kafka"]
merged = team_a.copy()
merged.extend(team_b)
print("Merged:", merged)
print("redis count:", merged.count("redis"))
unique = []
for item in merged:
    if item not in unique:
        unique.append(item)
unique.sort()
print("Unique sorted:", unique)

# ===== Task 3 =====
alerts = [(3, "Disk 80%"), (1, "DB down"), (2, "High latency"), (1, "Payment API 500s"), (4, "Cert expires in 20 days")]
alerts.sort()
while alerts and alerts[0][0] <= 2:
    severity, message = alerts.pop(0)
    print(f"Handling SEV-{severity}: {message}")
print("Left for later:", alerts)
