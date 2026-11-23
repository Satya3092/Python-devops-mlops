# Day 059 — Practice Tasks: Pathlib Module

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Path anatomy

**Problem statement:** For `Path("/home/ubuntu/projects/api/main.py")` print name, stem, suffix, parent and the grandparent (`parents[1]`).

**Input requirements:** No user input required.

**Expected behavior:** main.py, main, .py, /home/ubuntu/projects/api, /home/ubuntu/projects.

**Expected output:**

```text
main.py
main
.py
/home/ubuntu/projects/api
/home/ubuntu/projects
```

## Task 2 — Medium: Find Python files

**Problem statement:** Create `code_demo/` with nested folders containing 3 `.py` files and 2 `.md` files. Use `rglob` to print every `.py` file path relative to `code_demo`, sorted.

**Input requirements:** No user input required.

**Expected behavior:** Three relative paths.

**Expected output:**

```text
app/main.py
app/utils/helpers.py
tests/test_main.py
```

## Task 3 — Practical Challenge: Keep the newest backups

**Problem statement:** Create a folder `backups_demo` with 6 files `db-2026-11-15.sql.gz` … `db-2026-11-20.sql.gz`. Using pathlib, keep the newest 3 (by the date in the name) and delete the rest. Print what was deleted and what remains.

**Input requirements:** No user input required.

**Expected behavior:** Deletes 15–17, keeps 18–20.

**Expected output:**

```text
Deleted: db-2026-11-15.sql.gz
Deleted: db-2026-11-16.sql.gz
Deleted: db-2026-11-17.sql.gz
Remaining: ['db-2026-11-18.sql.gz', 'db-2026-11-19.sql.gz', 'db-2026-11-20.sql.gz']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
