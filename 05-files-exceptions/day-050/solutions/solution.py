"""
Day 050 — Working with CSV Files: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import csv

# ===== Task 1 =====
topics = ["File Handling Introduction", "Reading Files", "Writing Files", "Append Mode", "Working with CSV Files"]
with open("courses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["day", "topic"])
    for day, topic in zip(range(46, 51), topics):
        writer.writerow([day, topic])
with open("courses.csv", encoding="utf-8") as f:
    print(f.read(), end="")

# ===== Task 2 =====
scores = [("Asha", 91), ("Ravi", 78), ("Meera", 85), ("John", 66), ("Fatima", 94)]
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["student", "score"])
    writer.writerows(scores)
with open("scores.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
average = sum(int(r["score"]) for r in rows) / len(rows)
top = max(rows, key=lambda r: int(r["score"]))
print(f"Average: {average:.1f}")
print(f"Top: {top['student']} ({top['score']})")

# ===== Task 3 =====
groups = {}
with open("../../datasets/servers.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        groups.setdefault(row["environment"], []).append(row)
with open("env_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["environment", "servers", "avg_cpu", "critical_count"])
    writer.writeheader()
    for env, rows in groups.items():
        writer.writerow({
            "environment": env,
            "servers": len(rows),
            "avg_cpu": round(sum(int(r["cpu_usage"]) for r in rows) / len(rows), 1),
            "critical_count": sum(1 for r in rows if r["status"] == "critical"),
        })
with open("env_summary.csv", encoding="utf-8") as f:
    print(f.read(), end="")
