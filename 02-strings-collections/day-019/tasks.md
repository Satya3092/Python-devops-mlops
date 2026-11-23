# Day 019 — Practice Tasks: String Methods

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Clean user input

**Problem statement:** Given `env = "  StAgInG \n"`, produce `staging` and print whether it is one of dev/staging/prod.

**Input requirements:** No user input required.

**Expected behavior:** Prints `staging` and `Valid: True`.

**Expected output:**

```text
staging
Valid: True
```

## Task 2 — Medium: Parse key=value

**Problem statement:** Given the line `"DB_HOST=db.internal; DB_PORT=5432; DB_NAME=orders"`, split it into pairs and print each key and value on its own line, e.g. `DB_HOST -> db.internal`.

**Input requirements:** No user input required.

**Expected behavior:** Three lines of key -> value.

**Expected output:**

```text
DB_HOST -> db.internal
DB_PORT -> 5432
DB_NAME -> orders
```

## Task 3 — Practical Challenge: Process listing parser

**Problem statement:** Given a line of `ps aux` output `"www-data  1234  12.5  3.1  456789  65432 ?  S  10:01  0:42 nginx: worker process"`, extract the user, PID, CPU %, memory % and the command (everything from the 11th field). Print a summary and flag the process if CPU > 10.

**Input requirements:** No user input required.

**Expected behavior:** Prints user, PID, CPU, MEM, command and a high-CPU flag.

**Expected output:**

```text
User: www-data | PID: 1234 | CPU: 12.5 | MEM: 3.1
Command: nginx: worker process
FLAG: high CPU process -> 1234
```

<details><summary>💡 Hint</summary>

`split(maxsplit=10)` keeps the command in one piece.

</details>

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
