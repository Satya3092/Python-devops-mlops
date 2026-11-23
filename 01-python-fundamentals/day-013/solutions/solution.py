"""
Day 013 — if-else: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
score = int(input("Score: "))
print()
if score >= 50:
    print("Pass")
else:
    print("Fail")

# ===== Task 2 =====
http_code = 503
status = "UP" if http_code == 200 else "DOWN"
print("Status:", status)
if status == "UP":
    print("Action: No action")
else:
    print("Action: Restart service")

# ===== Task 3 =====
MIN_NODES, MAX_NODES = 2, 10
cpu = int(input("Average CPU %: "))
nodes = int(input("Current nodes: "))
print()
if cpu > 70:
    new_nodes = min(nodes + 1, MAX_NODES)
    print("Scaling out:", nodes, "->", new_nodes, "nodes (CPU", cpu, "% > 70 %)")
else:
    new_nodes = max(nodes - 1, MIN_NODES)
    print("Scaling in:", nodes, "->", new_nodes, "nodes (CPU", cpu, "% <= 70 %)")
