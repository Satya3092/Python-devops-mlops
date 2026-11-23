# Day 030 — Practice Tasks: While Loops

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Sum of digits

**Problem statement:** Use a while loop to compute the sum of the digits of 98765 (using `% 10` and `// 10`).

**Input requirements:** No user input required.

**Expected behavior:** Prints `Sum of digits: 35`.

**Expected output:**

```text
Sum of digits: 35
```

## Task 2 — Medium: Password prompt

**Problem statement:** Ask for a password up to 3 times. The correct password is `devops123`. Print `Access granted` or, after 3 failures, `Account locked`.

**Input requirements:** Up to three lines.

**Expected behavior:** Two failures then access granted.

**Sample input:**

```text
hello
admin
devops123
```

**Expected output:**

```text
Password: hello
Wrong password
Password: admin
Wrong password
Password: devops123
Access granted
```

## Task 3 — Practical Challenge: Queue consumer

**Problem statement:** Simulate a message queue `["order-1", "order-2", "POISON", "order-3"]`. Process messages from the front with `while queue:`. If a message is `POISON`, move it to a dead-letter list instead of processing. Print processed and dead-letter lists.

**Input requirements:** No user input required.

**Expected behavior:** Processed 3 orders, dead letter contains POISON.

**Expected output:**

```text
Processed: order-1
Processed: order-2
Moved to dead-letter queue: POISON
Processed: order-3
Processed: ['order-1', 'order-2', 'order-3']
Dead letter: ['POISON']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
