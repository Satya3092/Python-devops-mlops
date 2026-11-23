# Day 054 — Practice Tasks: Creating Custom Exceptions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Validate an email

**Problem statement:** Write `validate_email(email)` that raises `ValueError` if the email has no `@` or no `.` after the `@`. Test with three emails.

**Input requirements:** No user input required.

**Expected behavior:** One valid, two errors printed.

**Expected output:**

```text
asha@example.com is valid
Invalid: 'ravi.example.com': missing @
Invalid: 'meera@localhost': domain has no dot
```

## Task 2 — Medium: Quota exceeded

**Problem statement:** Create `QuotaExceededError`. Write `request_instances(current, requested, limit=20)` that raises it with a clear message when the limit would be exceeded, otherwise returns the new total. Handle it in the caller.

**Input requirements:** No user input required.

**Expected behavior:** One success and one quota error.

**Expected output:**

```text
New total: 15
Quota error: requested 4, but only 2 of 20 available
```

## Task 3 — Practical Challenge: Backup tool errors

**Problem statement:** Create a hierarchy `BackupError` → `SourceMissingError`, `InsufficientSpaceError` (store `needed_gb` and `free_gb`). Write `backup(source, size_gb, free_gb)` that raises the right error. Run three scenarios and handle each appropriately (print specific advice for space problems).

**Input requirements:** No user input required.

**Expected behavior:** Success, missing source, space problem with numbers.

**Expected output:**

```text
backed up /etc (1 GB)
SourceMissingError: /data does not exist
Space problem: need 120 GB, only 80 GB free. Free at least 40 GB.
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
