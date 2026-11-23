# Day 025 — Practice Tasks: Sets and Set Operations

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Remove duplicates

**Problem statement:** Given `tags = ["web", "prod", "web", "api", "prod", "linux"]`, print the unique tags sorted and how many duplicates were removed.

**Input requirements:** No user input required.

**Expected behavior:** `['api', 'linux', 'prod', 'web']` and `Removed 2 duplicates`.

**Expected output:**

```text
['api', 'linux', 'prod', 'web']
Removed 2 duplicates
```

## Task 2 — Medium: Skills gap

**Problem statement:** Given `my_skills = {"linux", "git", "docker", "kubernetes", "aws"}` and `mlops_skills = {"python", "docker", "kubernetes", "mlflow", "aws", "fastapi"}`, print what you already have, what you need to learn, and all skills combined.

**Input requirements:** No user input required.

**Expected behavior:** Three sorted lists.

**Expected output:**

```text
Already have: ['aws', 'docker', 'kubernetes']
Need to learn: ['fastapi', 'mlflow', 'python']
All skills: ['aws', 'docker', 'fastapi', 'git', 'kubernetes', 'linux', 'mlflow', 'python']
```

## Task 3 — Practical Challenge: Security group audit

**Problem statement:** Allowed ports policy: `{22, 80, 443}`. Two servers have open ports `web-01: {22, 80, 443, 8080}` and `web-02: {80, 443}`. For each server print unauthorised open ports, missing required ports (443 and 80 must be open), and a final COMPLIANT/NON-COMPLIANT verdict. Also print ports open on both servers.

**Input requirements:** No user input required.

**Expected behavior:** web-01 has unauthorised 8080 → NON-COMPLIANT; web-02 compliant; common ports {80, 443}.

**Expected output:**

```text
web-01: unauthorised=[8080] missing=[] -> NON-COMPLIANT
web-02: unauthorised=[] missing=[] -> COMPLIANT
Open on both: [80, 443]
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
