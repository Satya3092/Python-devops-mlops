# Day 048 — Writing Files

[⬅ Day 047](../../05-files-exceptions/day-047/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 049 ➡](../../05-files-exceptions/day-049/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create and overwrite files with mode `"w"`
- Use `write()`, `writelines()` and `print(file=...)`
- Generate configuration and report files from data

## 2. Topic Explanation

To write text, open a file in **write mode** `"w"`:

```python
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\n")
```

- `"w"` creates the file if missing and **truncates** (empties) it if it exists.
- `write(text)` writes a string and returns the number of characters written. It does **not** add a newline.
- `writelines(list_of_strings)` writes each string (you add the `\n`s).
- `print(..., file=f)` writes like print does, including the newline — very convenient.
- Use `"x"` mode to create a new file but fail if it already exists (safe for "never overwrite" cases).

**Generating files from data** is a core DevOps skill: inventories, `.env` files, nginx configs, Kubernetes manifests and HTML/Markdown reports are all just text you write.

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("text\n")
    f.writelines(["a\n", "b\n"])
    print("value", 42, file=f)
```

| Part | Meaning |
|---|---|
| `"w"` | Write mode: create or overwrite. |
| `"x"` | Exclusive create: error if the file exists. |
| `write(s)` | Writes a string; no automatic newline. |
| `writelines(list)` | Writes each string in a list. |
| `print(..., file=f)` | Print into a file instead of the screen. |

## 4. Example 1 — Basic Example: Three ways to write

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    chars = f.write("First line written with write()\n")
    f.writelines(["Second line\n", "Third line\n"])
    print("Fourth line via print, value =", 42, file=f)

print("write() returned:", chars, "characters")

with open("notes.txt", encoding="utf-8") as f:
    print(f.read(), end="")

# "w" overwrites everything
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Replaced!\n")
with open("notes.txt", encoding="utf-8") as f:
    print("After overwrite:", f.read().strip())
```

## 5. Example 2 — Practical Example: Generating an Ansible inventory and a .env file

```python
servers = [
    {"host": "web-01", "ip": "10.0.1.10", "group": "web"},
    {"host": "web-02", "ip": "10.0.1.11", "group": "web"},
    {"host": "db-01", "ip": "10.0.2.10", "group": "db"},
]

groups = {}
for s in servers:
    groups.setdefault(s["group"], []).append(s)

with open("inventory.ini", "w", encoding="utf-8") as inv:
    for group, members in groups.items():
        print(f"[{group}]", file=inv)
        for m in members:
            print(f"{m['host']} ansible_host={m['ip']}", file=inv)
        print(file=inv)                        # blank line between groups

settings = {"APP_ENV": "staging", "LOG_LEVEL": "INFO", "DB_HOST": "10.0.2.10", "DB_PORT": 5432}
with open(".env.example", "w", encoding="utf-8") as env_file:
    env_file.writelines(f"{key}={value}\n" for key, value in settings.items())

for name in ("inventory.ini", ".env.example"):
    print(f"----- {name} -----")
    with open(name, encoding="utf-8") as f:
        print(f.read().strip())
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `write()` returns the number of characters written.
- `print(..., file=f)` is handy because it adds spaces and the newline for you.
- Re-opening with `"w"` wipes the old content — be careful!

**Example 2**
- The data is grouped by role, then written as an Ansible INI inventory.
- `print(file=inv)` with no values writes an empty line.
- `writelines` receives a generator of `KEY=value\n` lines to create a `.env.example` file.

## 7. Expected Output

**Example 1:**

```text
write() returned: 32 characters
First line written with write()
Second line
Third line
Fourth line via print, value = 42
After overwrite: Replaced!
```

**Example 2:**

```text
----- inventory.ini -----
[web]
web-01 ansible_host=10.0.1.10
web-02 ansible_host=10.0.1.11

[db]
db-01 ansible_host=10.0.2.10
----- .env.example -----
APP_ENV=staging
LOG_LEVEL=INFO
DB_HOST=10.0.2.10
DB_PORT=5432
```

## 8. Common Mistakes

**1. Missing newlines**

`f.write("a"); f.write("b")` produces `ab`. Add `\n` or use `print(file=f)`.

**2. Writing non-strings**

`f.write(42)` → `TypeError`. Convert with `str()` or use an f-string.

**3. Writing secrets to disk**

Never write real passwords/keys into files committed to Git. Generate `.env.example` with placeholders and add `.env` to `.gitignore`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Multiplication file:** Write the multiplication table of 9 (1–10) to `table9.txt`, then print the file.
- **Task 2 (Medium) — Do not overwrite:** Use mode `"x"` to create `release_notes.txt`. Try to create it a second time and catch the `FileExistsError`, printing a friendly message.
- **Task 3 (Practical Challenge) — Generate an nginx upstream config:** Given backends `[("10.0.1.10", 8080), ("10.0.1.11", 8080), ("10.0.1.12", 8081)]`, generate `upstream.conf` containing an `upstream app_backend { ... }` block with one `server ip:port;` line each, plus `keepalive 32;`. Print the generated file.

## 10. DevOps/MLOps Connection

- **DevOps:** generating inventories, nginx/HAProxy configs, systemd units, Kubernetes YAML and Markdown/HTML reports from data.
- **Cloud:** writing user-data scripts, Terraform `.tfvars` files, or CSV cost reports.
- **MLOps:** writing metrics files (`metrics.json`) and run reports that CI pipelines publish as artefacts.

## 11. Interview Questions

**Q1. What does mode `x` do?**

<details><summary>Show answer</summary>

Creates a new file and raises `FileExistsError` if it already exists.

</details>

**Q2. Does `write()` add a newline?**

<details><summary>Show answer</summary>

No. You must include `\n` yourself.

</details>

**Q3. How would you write a file atomically so readers never see a half-written file?**

<details><summary>Show answer</summary>

Write to a temporary file in the same directory, then `os.replace(tmp, final)` which is an atomic rename.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 48 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 047](../../05-files-exceptions/day-047/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 049 ➡](../../05-files-exceptions/day-049/README.md)
