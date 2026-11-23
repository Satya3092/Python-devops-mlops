# Day 052 — Practice Tasks: Exception Handling

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Safe integer input

**Problem statement:** Ask the user for their age. If it is not a valid integer, print `Please enter a whole number` instead of crashing.

**Input requirements:** One line.

**Expected behavior:** Prints the friendly message.

**Sample input:**

```text
twenty
```

**Expected output:**

```text
Age: twenty
Please enter a whole number
```

## Task 2 — Medium: Safe list access

**Problem statement:** Write `get_item(items, index)` that returns the item or the string `out of range` when the index is invalid (catch `IndexError`). Test with indexes 0, 5 and -1 on `["a", "b", "c"]`.

**Input requirements:** No user input required.

**Expected behavior:** a, out of range, c.

**Expected output:**

```text
0 a
5 out of range
-1 c
```

## Task 3 — Practical Challenge: Config loader with clear errors

**Problem statement:** Write `load_port(path)` that reads a JSON file and returns `config["server"]["port"]` as an int. Handle: missing file, invalid JSON (`json.JSONDecodeError`), missing keys and a non-numeric port, returning `None` and printing a specific message for each. Test it with 4 small files you create in the solution.

**Input requirements:** No user input required.

**Expected behavior:** One success and three specific error messages.

**Expected output:**

```text
good.json -> 8080
missing.json: file not found
missing.json -> None
broken.json: invalid JSON (Illegal trailing comma before end of object)
broken.json -> None
nokey.json: missing key 'port'
nokey.json -> None
badport.json: port is not a number
badport.json -> None
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
