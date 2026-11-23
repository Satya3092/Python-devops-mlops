# Day 064 — Practice Tasks: Classes, Objects, and Constructors

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Rectangle

**Problem statement:** Create `Rectangle(width, height)` with `area()`, `perimeter()` and `__str__`. Create two rectangles and print them.

**Input requirements:** No user input required.

**Expected behavior:** Area/perimeter for both rectangles.

**Expected output:**

```text
Rectangle 3x4: area=12 perimeter=14
Rectangle 10x2: area=20 perimeter=24
```

## Task 2 — Medium: Service class

**Problem statement:** Create `Service(name, port, replicas=1)` with `scale(n)` (validate n ≥ 0), `url()` returning `http://<name>:<port>` and `__repr__`. Keep a class attribute listing all created service names.

**Input requirements:** No user input required.

**Expected behavior:** URLs, scaled replicas and the registry list.

**Expected output:**

```text
http://api:8080 http://worker:9000
Service(api, port=8080, replicas=4) Service(worker, port=9000, replicas=2)
Registry: ['api', 'worker']
```

## Task 3 — Practical Challenge: Inventory from JSON

**Problem statement:** Create a `@dataclass Host` with `name`, `ip`, `env` and `tags` (default empty list). Add a `classmethod` `from_json(text)` that returns a list of Host objects from a JSON array string. Load 3 hosts, then print hosts per environment and all hosts tagged `web`.

**Input requirements:** No user input required.

**Expected behavior:** Grouped hosts and the web-tagged ones.

**Expected output:**

```text
{'prod': ['web-01', 'db-01'], 'dev': ['web-dev']}
Web hosts: ['web-01', 'web-dev']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
