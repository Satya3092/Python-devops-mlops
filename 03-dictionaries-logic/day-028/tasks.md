# Day 028 — Practice Tasks: Nested Lists and Nested Dictionaries

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Classroom matrix

**Problem statement:** Store marks of 3 students in 3 subjects as a nested list. Print the second student's marks, the third subject mark of the first student, and each student's total.

**Input requirements:** No user input required.

**Expected behavior:** Totals per student.

**Expected output:**

```text
Student 2: [65, 70, 88]
Student 1, subject 3: 90
Student 1 total: 253
Student 2 total: 223
Student 3 total: 276
```

## Task 2 — Medium: Pod lookup

**Problem statement:** Given `cluster = {"nodes": [{"name": "node-1", "pods": ["api-1", "api-2"]}, {"name": "node-2", "pods": ["db-0"]}]}`, print every pod with its node name, then the total number of pods.

**Input requirements:** No user input required.

**Expected behavior:** Three lines `node-x: pod` and `Total pods: 3`.

**Expected output:**

```text
node-1: api-1
node-1: api-2
node-2: db-0
Total pods: 3
```

## Task 3 — Practical Challenge: Student Information System (Project 1 preview)

**Problem statement:** Store students as a list of dicts with `name`, `age` and `marks` (a dict of subject → mark). For each student, print the average mark and a grade (A ≥ 85, B ≥ 70, C ≥ 50, F). Finally print the class topper.

**Input requirements:** No user input required.

**Expected behavior:** Per-student averages/grades and the topper.

**Expected output:**

```text
Asha   avg=87.0 grade=A
Ravi   avg=70.3 grade=B
Meera  avg=50.7 grade=C
Topper: Asha (87.0)
```

<details><summary>💡 Hint</summary>

This is the core of [Project 1](../../projects/01-student-information-system/).

</details>

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
