# Day 040 — Practice Tasks: Keyword Arguments

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Order a pizza

**Problem statement:** Write `order_pizza(size, crust="thin", extra_cheese=False)` returning a description. Call it with keywords in a different order.

**Input requirements:** No user input required.

**Expected behavior:** Three descriptions.

**Expected output:**

```text
large pizza, thin crust, regular cheese
medium pizza, thin crust, with extra cheese
small pizza, stuffed crust, regular cheese
```

## Task 2 — Medium: Kubernetes scale command

**Problem statement:** Write `scale_command(deployment, *, replicas, namespace="default")` that returns `kubectl scale deployment/<d> --replicas=<n> -n <ns>`. Show that calling it without `replicas=` raises a TypeError.

**Input requirements:** No user input required.

**Expected behavior:** Two commands and the TypeError message.

**Expected output:**

```text
kubectl scale deployment/api --replicas=5 -n default
kubectl scale deployment/worker --replicas=2 -n jobs
TypeError: scale_command() takes 1 positional argument but 2 were given
```

## Task 3 — Practical Challenge: Safe delete helper

**Problem statement:** Write `delete_old_backups(backups, *, keep=3, dry_run=True)` where `backups` is a list of names sorted oldest→newest. It returns the list of backups it *would* delete and prints `Would delete ...` (dry run) or `Deleting ...`. Demonstrate both modes.

**Input requirements:** No user input required.

**Expected behavior:** Dry run lists deletions; real run prints Deleting lines.

**Expected output:**

```text
Would delete db-11-15.gz
Would delete db-11-16.gz
['db-11-15.gz', 'db-11-16.gz']
Deleting db-11-15.gz
['db-11-15.gz']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
