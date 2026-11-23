# Day 023 — Practice Tasks: List Methods

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Stack of commands

**Problem statement:** Use a list as a stack for an undo history: push `mkdir app`, `cd app`, `git init`, then pop twice and print what was undone and what remains.

**Input requirements:** No user input required.

**Expected behavior:** Undo `git init` and `cd app`, remaining `['mkdir app']`.

**Expected output:**

```text
Undo: git init
Undo: cd app
Remaining: ['mkdir app']
```

## Task 2 — Medium: Merge and dedupe

**Problem statement:** Merge `team_a = ["nginx", "redis"]` and `team_b = ["redis", "postgres", "nginx", "kafka"]` into one list with `extend`, count how many times `redis` appears, then build a sorted list without duplicates.

**Input requirements:** No user input required.

**Expected behavior:** Count 2 and `['kafka', 'nginx', 'postgres', 'redis']`.

**Expected output:**

```text
Merged: ['nginx', 'redis', 'redis', 'postgres', 'nginx', 'kafka']
redis count: 2
Unique sorted: ['kafka', 'nginx', 'postgres', 'redis']
```

## Task 3 — Practical Challenge: Priority alert queue

**Problem statement:** Alerts are tuples `(severity, message)` where 1 is most urgent: `[(3, "Disk 80%"), (1, "DB down"), (2, "High latency"), (1, "Payment API 500s"), (4, "Cert expires in 20 days")]`. Sort by severity, then process (pop from the front) only severity 1 and 2 alerts, printing each, and print what is left.

**Input requirements:** No user input required.

**Expected behavior:** Processes the two SEV-1 and one SEV-2 alerts; two remain.

**Expected output:**

```text
Handling SEV-1: DB down
Handling SEV-1: Payment API 500s
Handling SEV-2: High latency
Left for later: [(3, 'Disk 80%'), (4, 'Cert expires in 20 days')]
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
