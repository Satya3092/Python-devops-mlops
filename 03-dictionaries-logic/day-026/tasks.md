# Day 026 — Practice Tasks: Dictionaries

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Book record

**Problem statement:** Create a dict for a book (title, author, year). Print each field, then add `rating`, update `year` and print the dict.

**Input requirements:** No user input required.

**Expected behavior:** Shows the updated dictionary.

**Expected output:**

```text
Title: The Phoenix Project
Author: Gene Kim
Year: 2013
{'title': 'The Phoenix Project', 'author': 'Gene Kim', 'year': 2018, 'rating': 5}
```

## Task 2 — Medium: Port lookup

**Problem statement:** Create a dict mapping service names to ports (ssh 22, http 80, https 443, postgres 5432, redis 6379). Look up `postgres` with `[]`, and `mongodb` with `.get()` returning `unknown`. Print how many services are known.

**Input requirements:** No user input required.

**Expected behavior:** 5432, unknown, 5 services.

**Expected output:**

```text
postgres: 5432
mongodb: unknown
Known services: 5
```

## Task 3 — Practical Challenge: Environment config merge

**Problem statement:** You have `defaults = {"replicas": 1, "log_level": "INFO", "debug": False}` and `prod_overrides = {"replicas": 5, "log_level": "WARNING"}`. Create a final config where overrides win (copy defaults, then assign each override key). Print the final config and which keys were overridden.

**Input requirements:** No user input required.

**Expected behavior:** Final config with replicas 5, WARNING, debug False; overridden: replicas, log_level.

**Expected output:**

```text
Final config: {'replicas': 5, 'log_level': 'WARNING', 'debug': False}
Overridden keys: ['replicas', 'log_level']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
