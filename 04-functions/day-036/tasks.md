# Day 036 — Practice Tasks: Introduction to Functions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Say hello

**Problem statement:** Write a function `say_hello()` that prints three lines introducing the course, and call it twice.

**Input requirements:** No user input required.

**Expected behavior:** Six lines printed.

**Expected output:**

```text
Hello!
Welcome to 100 Days of Python.
From beginner to MLOps.
Hello!
Welcome to 100 Days of Python.
From beginner to MLOps.
```

## Task 2 — Medium: Separator helper

**Problem statement:** Write `print_separator()` that prints 40 dashes. Use it to separate three sections (Linux, Docker, Kubernetes) where each section prints one fact.

**Input requirements:** No user input required.

**Expected behavior:** Sections divided by dash lines.

**Expected output:**

```text
----------------------------------------
Linux: everything is a file
----------------------------------------
Docker: containers share the host kernel
----------------------------------------
Kubernetes: the smallest deployable unit is a pod
----------------------------------------
```

## Task 3 — Practical Challenge: Refactor a deployment script

**Problem statement:** Turn this flat script into functions `pull_code()`, `run_tests()`, `build_image()`, `deploy()` and a `main()` that calls them in order. Each function prints what it does, e.g. `[1/4] Pulling latest code from main`. Add a docstring to each function.

**Input requirements:** No user input required.

**Expected behavior:** Four ordered steps and a final `Deployment pipeline finished`.

**Expected output:**

```text
[1/4] Pulling latest code from main
[2/4] Running unit tests
[3/4] Building Docker image
[4/4] Deploying to Kubernetes
Deployment pipeline finished
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
