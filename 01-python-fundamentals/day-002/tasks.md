# Day 002 — Practice Tasks: Variables and Naming Conventions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Personal profile

**Problem statement:** Create variables `full_name`, `city`, `years_experience` and `favourite_tool`, then print each one with a label.

**Input requirements:** No user input required.

**Expected behavior:** Four labelled lines are printed.

**Expected output:**

```text
Name: Satya Prakash Singh
City: Bengaluru
Experience (years): 10
Favourite tool: Kubernetes
```

## Task 2 — Medium: Swap two values

**Problem statement:** You have `primary_db = "db-01"` and `replica_db = "db-02"`. A failover happened: swap the values so the replica becomes primary. Print before and after.

**Input requirements:** No user input required.

**Expected behavior:** The values are swapped without retyping the strings.

**Expected output:**

```text
Before -> primary: db-01 | replica: db-02
After  -> primary: db-02 | replica: db-01
```

<details><summary>💡 Hint</summary>

Python can do `a, b = b, a`.

</details>

## Task 3 — Practical Challenge: Docker run summary

**Problem statement:** Store container settings in well-named variables (image name, tag, container name, host port, container port, restart policy). Use a constant for the registry `REGISTRY = "docker.io"`. Print a summary and the equivalent `docker run` command built from the variables.

**Input requirements:** No user input required.

**Expected behavior:** The printed command uses the variable values, e.g. `docker run -d --name web -p 8080:80 --restart always docker.io/nginx:1.27`.

**Expected output:**

```text
Image: docker.io/nginx:1.27
Container: web
Ports: 8080 -> 80
Command:
docker run -d --name web -p 8080:80 --restart always docker.io/nginx:1.27
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
