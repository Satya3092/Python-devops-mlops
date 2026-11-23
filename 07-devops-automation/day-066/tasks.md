# Day 066 — Practice Tasks: Python System Administration Automation

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Facts summary

**Problem statement:** Print a one-line summary like `ubuntu@web-01 | Linux 6.8 | 4 CPUs | Python 3.12.3` using `getpass`, `socket`, `platform` and `os`.

**Input requirements:** No user input required.

**Expected behavior:** One summary line about your machine.

**Expected output:**

```text
ubuntu@ip-10-0-1-25 | Linux 6.8 | 2 CPUs | Python 3.12.3
```

## Task 2 — Medium: Users with login shells (Linux)

**Problem statement:** Parse a sample `/etc/passwd` content (given as a string in the solution) and list users whose shell is `/bin/bash` or `/bin/zsh` with their UID and home directory. Skip system users (UID < 1000) except root.

**Input requirements:** No user input required.

**Expected behavior:** root plus the two human users.

**Expected output:**

```text
root     uid=0     home=/root
ubuntu   uid=1000  home=/home/ubuntu
asha     uid=1001  home=/home/asha
```

## Task 3 — Practical Challenge: Idempotent hosts-file manager

**Problem statement:** Write `ensure_host_entry(path, ip, hostname)` that adds `ip hostname` to a hosts-style file only if that hostname isn't already present, and updates the IP if the hostname exists with a different IP. Return `added`, `updated` or `unchanged`. Demonstrate all three on a sample file.

**Input requirements:** No user input required.

**Expected behavior:** added → unchanged → updated, then prints the file.

**Expected output:**

```text
added
unchanged
updated
127.0.0.1 localhost
10.0.0.21 db.internal
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
