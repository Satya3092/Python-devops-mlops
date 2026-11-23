"""
Day 028 — Nested Lists and Nested Dictionaries: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
marks = [[78, 85, 90], [65, 70, 88], [92, 95, 89]]
print("Student 2:", marks[1])
print("Student 1, subject 3:", marks[0][2])
for index, row in enumerate(marks, start=1):
    print(f"Student {index} total: {sum(row)}")

# ===== Task 2 =====
cluster = {"nodes": [{"name": "node-1", "pods": ["api-1", "api-2"]}, {"name": "node-2", "pods": ["db-0"]}]}
total = 0
for node in cluster["nodes"]:
    for pod in node["pods"]:
        print(f"{node['name']}: {pod}")
        total += 1
print("Total pods:", total)

# ===== Task 3 =====
students = [
    {"name": "Asha", "age": 21, "marks": {"python": 92, "linux": 88, "cloud": 81}},
    {"name": "Ravi", "age": 23, "marks": {"python": 67, "linux": 74, "cloud": 70}},
    {"name": "Meera", "age": 22, "marks": {"python": 45, "linux": 58, "cloud": 49}},
]
topper_name, topper_avg = "", 0
for student in students:
    average = sum(student["marks"].values()) / len(student["marks"])
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 50:
        grade = "C"
    else:
        grade = "F"
    print(f"{student['name']:<6} avg={average:.1f} grade={grade}")
    if average > topper_avg:
        topper_name, topper_avg = student["name"], average
print(f"Topper: {topper_name} ({topper_avg:.1f})")
