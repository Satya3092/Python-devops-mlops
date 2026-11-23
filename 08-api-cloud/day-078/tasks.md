# Day 078 — Practice Tasks: Working with APIs using Requests

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Health checker

**Problem statement:** Write `is_healthy(base_url)` that returns True only if `/health` answers 200 with `{"status": "ok"}` within 2 seconds, and False for any exception. Test it on the mock API and on `http://127.0.0.1:9`.

**Input requirements:** No user input required.

**Expected behavior:** True then False.

**Expected output:**

```text
True False
```

## Task 2 — Medium: Server summary

**Problem statement:** Fetch all servers and print the count per environment and the total CPU of running servers.

**Input requirements:** No user input required.

**Expected behavior:** Counts per env and total running CPU.

**Expected output:**

```text
{'prod': 2, 'dev': 1}
Running CPU: 8
```

## Task 3 — Practical Challenge: Extend the client

**Problem statement:** Add `create_server(name, env, cpu=2)` and `delete_server(id)` methods to a copy of `InventoryClient` (using `session.post(json=...)` and `session.delete`). Create a server, read it back, delete it, and confirm `server(id)` returns None afterwards.

**Input requirements:** No user input required.

**Expected behavior:** Create → read → delete → None.

**Expected output:**

```text
Created: {'id': 4, 'name': 'ml-gpu-01', 'env': 'dev', 'cpu': 16, 'status': 'provisioning'}
Read back: {'id': 4, 'name': 'ml-gpu-01', 'env': 'dev', 'cpu': 16, 'status': 'provisioning'}
Delete status: 204
After delete: None
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
