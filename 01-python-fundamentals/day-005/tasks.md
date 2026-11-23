# Day 005 — Practice Tasks: Input and Output

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Greeting

**Problem statement:** Ask the user for their name and favourite DevOps tool, then print `Hi <name>! <tool> is a great choice.`

**Input requirements:** Two lines: a name and a tool.

**Expected behavior:** A single greeting line.

**Sample input:**

```text
Asha
Terraform
```

**Expected output:**

```text
Your name: Asha
Favourite DevOps tool: Terraform

Hi Asha! Terraform is a great choice.
```

## Task 2 — Medium: CSV line builder

**Problem statement:** Ask for hostname, IP and OS. Print them as one CSV line using `sep=","`.

**Input requirements:** Three lines.

**Expected behavior:** Prints `web-01,10.0.0.5,Ubuntu 24.04`.

**Sample input:**

```text
web-01
10.0.0.5
Ubuntu 24.04
```

**Expected output:**

```text
Hostname: web-01
IP: 10.0.0.5
OS: Ubuntu 24.04

web-01,10.0.0.5,Ubuntu 24.04
```

## Task 3 — Practical Challenge: Git commit wizard

**Problem statement:** Ask for a change type (feat/fix/docs), a scope and a short message. Print a Conventional Commit message `type(scope): message` and the full `git commit -m "..."` command.

**Input requirements:** Three lines.

**Expected behavior:** Prints the commit message and command.

**Sample input:**

```text
feat
auth
add token refresh
```

**Expected output:**

```text
Type (feat/fix/docs): feat
Scope: auth
Message: add token refresh

Commit message: feat(auth): add token refresh
git commit -m "feat(auth): add token refresh"
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
