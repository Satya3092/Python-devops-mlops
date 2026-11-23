# Project 1 — Python Student Information System

**Phase:** after Day 28 · **Difficulty:** 🟢 Beginner · **Concepts:** variables, input, conditions, lists, dictionaries, loops

A menu-driven command-line program to manage students and their marks — your first complete Python application.

## Features
- Add a student (name, age, course) with input validation
- Record marks for subjects
- List all students in a formatted table
- Search a student by name (case-insensitive)
- Show statistics: average per student, grade, class topper, subject averages
- Delete a student
- Everything stored in a **list of dictionaries** (no files or classes yet)

## Data structure
```python
students = [
    {"id": 1, "name": "Asha", "age": 21, "course": "DevOps",
     "marks": {"python": 92, "linux": 88}},
]
```

## Run it
```bash
python student_system.py
```

Sample session:
```text
===== Student Information System =====
1. Add student      2. Add marks     3. List students
4. Search student   5. Statistics    6. Delete student
0. Exit
Choose an option: 3
ID  NAME      AGE  COURSE        AVG  GRADE
1   Asha       21  DevOps       90.0  A
2   Ravi       23  Cloud        70.5  B
```

The program starts with two sample students so you can try every option immediately.

## Concepts used
| Concept | Where |
|---|---|
| Variables & input | reading menu choices and student data |
| Type conversion & validation | `int(input())` inside `while True` loops |
| Conditions | menu dispatch, grade calculation |
| Lists | the `students` list |
| Dictionaries | each student, and their `marks` |
| Loops | menu loop, table printing, statistics |

## Extend it (challenges)
1. Save and load students from a JSON file (Day 51).
2. Move each menu option into a function (Day 36) — then into a `Student` class (Day 64).
3. Export a CSV report (Day 50).
