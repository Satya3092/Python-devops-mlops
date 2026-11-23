# Day 067 — Practice Tasks: Working with Environment Variables

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Greeting from env

**Problem statement:** Read `USER_NAME` from the environment (default `stranger`) and print `Hello, <name>!`. Run it once without and once after setting `os.environ["USER_NAME"]`.

**Input requirements:** No user input required.

**Expected behavior:** `Hello, stranger!` then `Hello, Asha!`.

**Expected output:**

```text
Hello, stranger!
Hello, Asha!
```

## Task 2 — Medium: Typed config reader

**Problem statement:** Write `env_int(name, default)` and `env_bool(name, default)` helpers that convert values and fall back to the default (with a warning) on invalid input. Test with `MAX_RETRIES=5`, `TIMEOUT=abc`, `VERBOSE=yes`.

**Input requirements:** No user input required.

**Expected behavior:** 5, default timeout with a warning, True.

**Expected output:**

```text
WARNING: TIMEOUT='abc' is not an int, using 30
5 30 True
```

## Task 3 — Practical Challenge: Config validator for a container

**Problem statement:** Given a list of required variables `["DB_HOST", "DB_USER", "DB_PASSWORD", "REDIS_URL"]`, write `validate_env(required)` that returns missing names. Set some of them, print a start-up report that masks any variable containing `PASSWORD`, `SECRET` or `TOKEN`, and exit with code 1 (use `SystemExit`) if anything is missing — catch it in the solution to show the message.

**Input requirements:** No user input required.

**Expected behavior:** Masked report, list of missing variables, exit code 1.

**Expected output:**

```text
DB_HOST      = db.internal
DB_USER      = app
DB_PASSWORD  = ****
REDIS_URL    = <missing>
Missing variables: ['REDIS_URL'] -> exit code 1
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
