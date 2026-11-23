# Day 005 — Input and Output

[⬅ Day 004](../../01-python-fundamentals/day-004/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 006 ➡](../../01-python-fundamentals/day-006/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read user input with `input()`
- Control `print()` output using `sep` and `end`
- Understand that `input()` always returns a string

## 2. Topic Explanation

Programs talk to people through **input** (data coming in) and **output** (data going out).

- `print()` sends output to the screen (called **standard output** or *stdout* — the same stream `echo` writes to).
- `input("prompt")` shows a prompt, waits for the user to type and press Enter, then **returns the typed text as a string**.

`print()` has two handy options:
- `sep="..."` — what to put **between** values (default is a space).
- `end="..."` — what to put **at the end** (default is a newline `\n`).

Analogy: `input()` is like `read` in Bash: `read -p "Name: " name`.

Important: whatever the user types — even `42` — comes back as text `"42"`. Converting it to a number is tomorrow's lesson.

## 3. Syntax

```python
variable = input("Prompt text: ")
print(value1, value2, sep=" ", end="\n")
```

| Part | Meaning |
|---|---|
| `input(prompt)` | Displays `prompt`, waits for Enter, returns the typed text (`str`). |
| `print(...)` | Writes values to standard output. |
| `sep` | Separator placed between values. Default `' '`. |
| `end` | Text printed after the last value. Default `'\n'` (new line). |

## 4. Example 1 — Basic Example: Asking for a name

```python
name = input("What is your name? ")
print("Hello,", name)
print("Welcome to Day 5!")
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

## 5. Example 2 — Practical Example: Collecting deployment details

```python
# Interactive prompt, like a small deployment wizard
app_name = input("Application name: ")
version = input("Version to deploy: ")
environment = input("Target environment: ")

print()                                              # empty line
print("Deployment summary")
print("App", "Version", "Env", sep=" | ")
print(app_name, version, environment, sep=" | ")
print("Image tag: ", app_name, ":", version, sep="")  # no spaces
print("Deploying", end="")                           # stay on same line
print("...", end="")
print(" done")
print("input() returns:", type(version))
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `input("What is your name? ")` prints the prompt and pauses. The typed text is stored in `name`.

**Example 2**
- Three `input()` calls collect three answers in order.
- `print()` with no arguments prints an empty line.
- `sep=" | "` puts ` | ` between the values, producing a table-like row.
- `sep=""` removes spaces so `billing-api:2.4.1` is glued together.
- `end=""` stops `print` from moving to a new line, so the next print continues the same line.
- The last line proves `input()` returns a `str` even though we typed numbers.

## 7. Expected Output

**Example 1:**

```text
What is your name? Satya
Hello, Satya
Welcome to Day 5!
```

**Example 2:**

```text
Application name: billing-api
Version to deploy: 2.4.1
Target environment: staging

Deployment summary
App | Version | Env
billing-api | 2.4.1 | staging
Image tag: billing-api:2.4.1
Deploying... done
input() returns: <class 'str'>
```

## 8. Common Mistakes

**1. Doing maths on `input()` directly**

`age = input(); age + 1` raises `TypeError` because `age` is a string. Use `int(input())` (Day 6).

**2. Forgetting the space in the prompt**

`input("Name:")` makes the cursor stick to the colon. End prompts with a space: `"Name: "`.

**3. Using `input()` in automation**

Scripts run by cron or CI have no one to type. Use command-line arguments (Day 68) or environment variables (Day 67) for automation.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Greeting:** Ask the user for their name and favourite DevOps tool, then print `Hi <name>! <tool> is a great choice.`
- **Task 2 (Medium) — CSV line builder:** Ask for hostname, IP and OS. Print them as one CSV line using `sep=","`.
- **Task 3 (Practical Challenge) — Git commit wizard:** Ask for a change type (feat/fix/docs), a scope and a short message. Print a Conventional Commit message `type(scope): message` and the full `git commit -m "..."` command.

## 10. DevOps/MLOps Connection

- **DevOps:** Interactive setup scripts (bootstrap a new laptop, create a new microservice skeleton) use `input()`. Production automation should **not** — it must run unattended.
- **Output** is what lands in your CI logs, so formatting it clearly (`sep`, `end`) makes pipelines easier to debug.
- **MLOps:** Later you will replace `input()` with an HTTP API (FastAPI, Day 98) — the API's request body is the "input" for your model.

## 11. Interview Questions

**Q1. What type does `input()` return?**

<details><summary>Show answer</summary>

Always `str`, regardless of what the user types.

</details>

**Q2. How do you print without a newline at the end?**

<details><summary>Show answer</summary>

`print(value, end="")`.

</details>

**Q3. Where does `print()` write, and how can you redirect it in Linux?**

<details><summary>Show answer</summary>

To standard output (stdout). In the shell you can redirect with `python app.py > out.txt` or pipe with `|`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 5 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 004](../../01-python-fundamentals/day-004/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 006 ➡](../../01-python-fundamentals/day-006/README.md)
