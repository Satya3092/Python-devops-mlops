"""
Day 021 — Lists: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
team = ["Asha", "Ravi", "Meera"]
team.append("John")
team.append("Fatima")
team[1] = "Karan"
team.remove(team[-1])
print(team)
print("Members:", len(team))

# ===== Task 2 =====
open_ports = [22, 80, 443, 3306, 8080, 22]
print("Count:", len(open_ports))
print("Highest:", max(open_ports))
print("MySQL exposed:", 3306 in open_ports)
print("Sorted:", sorted(open_ports))
print("Original:", open_ports)

# ===== Task 3 =====
durations = [312, 298, 1045, 305, 287, 330, 299]
average = sum(durations) / len(durations)
print(f"min={min(durations)} max={max(durations)} avg={average:.1f}")
outliers = []
normal = []
for d in durations:
    if d > 1.5 * average:
        outliers.append(d)
    else:
        normal.append(d)
print("Outliers:", outliers)
print(f"Average without outliers: {sum(normal) / len(normal):.1f}")
