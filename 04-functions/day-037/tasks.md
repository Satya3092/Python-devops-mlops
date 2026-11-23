# Day 037 — Practice Tasks: Function Parameters and Arguments

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Area of a rectangle

**Problem statement:** Write `print_area(width, height)` that prints the area. Call it for 5×3 and 12×7.

**Input requirements:** No user input required.

**Expected behavior:** `Area: 15` and `Area: 84`.

**Expected output:**

```text
Area: 15
Area: 84
```

## Task 2 — Medium: SSH command builder

**Problem statement:** Write `print_ssh_command(user, host, port)` that prints `ssh -p <port> <user>@<host>`. Call it for three servers.

**Input requirements:** No user input required.

**Expected behavior:** Three ssh commands.

**Expected output:**

```text
ssh -p 22 ubuntu@10.0.0.5
ssh -p 2222 ec2-user@bastion.example.com
ssh -p 22 admin@db-01.internal
```

## Task 3 — Practical Challenge: Log line formatter

**Problem statement:** Write `log(level, service, message)` that prints `[LEVEL] service: message` with the level upper-cased and padded to 7 characters inside the brackets. Also write `log_many(level, service, messages)` that calls `log` for each message in a list.

**Input requirements:** No user input required.

**Expected behavior:** Formatted log lines.

**Expected output:**

```text
[INFO   ] auth: user logged in
[ERROR  ] payments: card declined
[WARNING] orders: slow query
[WARNING] orders: retrying request
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
