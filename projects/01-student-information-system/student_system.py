"""
Project 1 - Student Information System (Phase 1-3 concepts only).

Run:  python student_system.py
"""

students = [
    {"id": 1, "name": "Asha", "age": 21, "course": "DevOps", "marks": {"python": 92, "linux": 88}},
    {"id": 2, "name": "Ravi", "age": 23, "course": "Cloud", "marks": {"python": 67, "linux": 74}},
]
next_id = 3

MENU = """
===== Student Information System =====
1. Add student      2. Add marks     3. List students
4. Search student   5. Statistics    6. Delete student
0. Exit"""

while True:
    print(MENU)
    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Name: ").strip().title()
        if not name:
            print("Name cannot be empty.")
            continue
        age_text = input("Age: ").strip()
        if not age_text.isdigit() or not 15 <= int(age_text) <= 80:
            print("Age must be a number between 15 and 80.")
            continue
        course = input("Course: ").strip() or "General"
        students.append({"id": next_id, "name": name, "age": int(age_text), "course": course, "marks": {}})
        print(f"Added {name} with id {next_id}.")
        next_id += 1

    elif choice == "2":
        id_text = input("Student id: ").strip()
        student = None
        for s in students:
            if id_text.isdigit() and s["id"] == int(id_text):
                student = s
        if student is None:
            print("No student with that id.")
            continue
        subject = input("Subject: ").strip().lower()
        mark_text = input("Mark (0-100): ").strip()
        if not mark_text.isdigit() or int(mark_text) > 100:
            print("Mark must be a whole number from 0 to 100.")
            continue
        student["marks"][subject] = int(mark_text)
        print(f"Saved {subject}={mark_text} for {student['name']}.")

    elif choice == "3":
        if not students:
            print("No students yet.")
            continue
        print(f"{'ID':<4}{'NAME':<10}{'AGE':>3}  {'COURSE':<12}{'AVG':>5}  GRADE")
        for s in students:
            marks = list(s["marks"].values())
            average = sum(marks) / len(marks) if marks else 0
            if not marks:
                grade = "-"
            elif average >= 85:
                grade = "A"
            elif average >= 70:
                grade = "B"
            elif average >= 50:
                grade = "C"
            else:
                grade = "F"
            print(f"{s['id']:<4}{s['name']:<10}{s['age']:>3}  {s['course']:<12}{average:>5.1f}  {grade}")

    elif choice == "4":
        term = input("Search name: ").strip().lower()
        found = [s for s in students if term in s["name"].lower()]
        if not found:
            print("No match.")
        for s in found:
            print(f"{s['id']}: {s['name']} ({s['age']}), {s['course']}, marks={s['marks']}")

    elif choice == "5":
        graded = [s for s in students if s["marks"]]
        if not graded:
            print("No marks recorded yet.")
            continue
        best_name, best_avg = "", -1
        subject_totals = {}
        for s in graded:
            average = sum(s["marks"].values()) / len(s["marks"])
            if average > best_avg:
                best_name, best_avg = s["name"], average
            for subject, mark in s["marks"].items():
                subject_totals.setdefault(subject, []).append(mark)
        print(f"Students: {len(students)} (with marks: {len(graded)})")
        print(f"Topper: {best_name} ({best_avg:.1f})")
        for subject, marks in sorted(subject_totals.items()):
            print(f"  {subject:<10} average {sum(marks) / len(marks):.1f} over {len(marks)} student(s)")

    elif choice == "6":
        id_text = input("Student id to delete: ").strip()
        before = len(students)
        students = [s for s in students if not (id_text.isdigit() and s["id"] == int(id_text))]
        print("Deleted." if len(students) < before else "No student with that id.")

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option, please choose 0-6.")
