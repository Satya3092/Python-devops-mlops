# Day 051 — Practice Tasks: Working with JSON

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Dict to JSON

**Problem statement:** Convert a dict describing yourself (name, skills list, years, learning_python=True) to a pretty JSON string and print it.

**Input requirements:** No user input required.

**Expected behavior:** Indented JSON with `true`.

**Expected output:**

```text
{
  "name": "Satya",
  "skills": [
    "linux",
    "docker",
    "kubernetes"
  ],
  "years": 10,
  "learning_python": true
}
```

## Task 2 — Medium: Parse an API response

**Problem statement:** Parse this JSON string: `{"pods": [{"name": "api-1", "status": "Running"}, {"name": "api-2", "status": "Pending"}, {"name": "db-0", "status": "Running"}]}` and print the names of running pods and the count of non-running pods.

**Input requirements:** No user input required.

**Expected behavior:** `['api-1', 'db-0']` and `Not running: 1`.

**Expected output:**

```text
['api-1', 'db-0']
Not running: 1
```

## Task 3 — Practical Challenge: Feature-flag manager

**Problem statement:** Create `flags.json` with flags `{"dark_mode": false, "new_checkout": true, "beta_search": false}`. Write functions `load_flags(path)`, `save_flags(path, flags)` and `toggle(path, name)` (which loads, flips one flag, saves, and returns the new value; unknown flags raise `KeyError`). Toggle two flags and print the final file.

**Input requirements:** No user input required.

**Expected behavior:** Two flags flipped; final JSON printed.

**Expected output:**

```text
dark_mode -> True
new_checkout -> False
{
  "dark_mode": true,
  "new_checkout": false,
  "beta_search": false
}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
