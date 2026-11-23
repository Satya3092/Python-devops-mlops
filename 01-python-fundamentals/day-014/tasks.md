# Day 014 — Practice Tasks: elif and Nested Conditions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Traffic light

**Problem statement:** Ask for a colour (red/yellow/green) and print Stop / Slow down / Go, or `Invalid colour`.

**Input requirements:** One word.

**Expected behavior:** Prints `Slow down`.

**Sample input:**

```text
yellow
```

**Expected output:**

```text
Colour: yellow

Slow down
```

## Task 2 — Medium: HTTP status explainer

**Problem statement:** Given `status_code = 404`, print the category: 1xx Informational, 2xx Success, 3xx Redirection, 4xx Client Error, 5xx Server Error, otherwise Unknown. Inside 4xx, print a special note for 401 / 403 / 404.

**Input requirements:** No user input required.

**Expected behavior:** Prints `Client Error` and `Not Found: check the URL`.

**Expected output:**

```text
Client Error
Not Found: check the URL
```

## Task 3 — Practical Challenge: Server health classifier

**Problem statement:** Ask for CPU %, memory % and disk %. Classify the server as CRITICAL if any value >= 90, WARNING if any >= 75, otherwise HEALTHY. Additionally, if CRITICAL and disk is the cause, print `Suggested action: clean /var/log`.

**Input requirements:** Three integers.

**Expected behavior:** Prints CRITICAL and the suggested action.

**Sample input:**

```text
62
71
93
```

**Expected output:**

```text
CPU %: 62
Memory %: 71
Disk %: 93

Status: CRITICAL
Suggested action: clean /var/log
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
