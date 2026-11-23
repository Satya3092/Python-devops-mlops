# Day 028 — Nested Lists and Nested Dictionaries

[⬅ Day 027](../../03-dictionaries-logic/day-027/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 029 ➡](../../03-dictionaries-logic/day-029/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read and update data in nested lists and dictionaries
- Loop through lists of dictionaries (JSON-style data)
- Navigate deeply nested data safely

## 2. Topic Explanation

Real-world data is **nested**: lists inside dicts inside lists. A Kubernetes manifest, an AWS API response or a JSON config file all look like this.

```python
cluster = {
    "name": "prod-cluster",
    "nodes": [
        {"name": "node-1", "pods": ["api", "worker"]},
        {"name": "node-2", "pods": ["db"]},
    ],
}
cluster["nodes"][0]["pods"][1]   # -> "worker"
```

Read the path left to right: *cluster → nodes list → first node → pods list → second pod*.

**Nested lists** represent tables/matrices: `grid[row][column]`.

Tips:
- Print intermediate levels while exploring unfamiliar data.
- Use `.get()` at each level for optional keys: `data.get("spec", {}).get("replicas", 1)`.
- A **list of dicts** is the most common shape — each dict is a record (like a table row).

## 3. Syntax

```python
value = data["key"][index]["other_key"]
matrix[row][col]
for record in list_of_dicts:
    print(record["field"])
safe = data.get("a", {}).get("b", default)
```

| Part | Meaning |
|---|---|
| `data["k"][i]` | Chain keys and indexes to drill down. |
| `matrix[r][c]` | Row r, column c of a nested list. |
| `list of dicts` | Each dict is one record; loop over the list. |
| `.get(k, {})` | Return an empty dict when missing so the next `.get` still works. |

## 4. Example 1 — Basic Example: Nested list (matrix) and nested dict

```python
# CPU usage of 3 servers measured at 4 points in time
cpu_matrix = [
    [20, 35, 50, 40],   # web-01
    [70, 85, 90, 95],   # web-02
    [10, 15, 12, 18],   # db-01
]
print("web-02 at time 3:", cpu_matrix[1][2])
print("All readings for db-01:", cpu_matrix[2])
print("Max of web-02:", max(cpu_matrix[1]))

user = {
    "name": "asha",
    "groups": ["devops", "docker"],
    "address": {"city": "Pune", "country": "India"},
}
print("City:", user["address"]["city"])
print("First group:", user["groups"][0])
user["groups"].append("sudo")
print("Groups now:", user["groups"])
```

## 5. Example 2 — Practical Example: Exploring a cloud-style inventory response

```python
inventory = {
    "region": "ap-south-1",
    "instances": [
        {"id": "i-001", "type": "t3.micro", "state": "running",
         "tags": {"Name": "web-01", "Env": "prod"}},
        {"id": "i-002", "type": "t3.large", "state": "stopped",
         "tags": {"Name": "batch-01", "Env": "dev"}},
        {"id": "i-003", "type": "m5.xlarge", "state": "running",
         "tags": {"Name": "db-01"}},                  # no Env tag!
    ],
}

print(f"Region: {inventory['region']}")
print(f"{'ID':<7}{'NAME':<10}{'TYPE':<11}{'STATE':<9}ENV")
running_count = 0
for instance in inventory["instances"]:
    name = instance["tags"].get("Name", "-")
    env = instance["tags"].get("Env", "MISSING")
    print(f"{instance['id']:<7}{name:<10}{instance['type']:<11}{instance['state']:<9}{env}")
    if instance["state"] == "running":
        running_count += 1

print("Running instances:", running_count)
untagged = [i["id"] for i in inventory["instances"] if "Env" not in i["tags"]]
print("Instances missing an Env tag:", untagged)

# Safe navigation for optional nested keys
monitoring = inventory.get("settings", {}).get("monitoring", "disabled")
print("Monitoring:", monitoring)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `cpu_matrix[1][2]` → row 1 (web-02), column 2 (third reading) → 90.
- `user["address"]["city"]` drills two dict levels; `user["groups"].append(...)` modifies the inner list in place.

**Example 2**
- The structure mimics a boto3 `describe_instances` response: a dict containing a list of dicts containing dicts.
- The loop treats each instance dict as a row. `instance["tags"].get("Env", "MISSING")` handles absent tags.
- A list comprehension (Day 34) finds instances without an `Env` tag — a common compliance check.
- `inventory.get("settings", {}).get(...)` never crashes even though `settings` does not exist.

## 7. Expected Output

**Example 1:**

```text
web-02 at time 3: 90
All readings for db-01: [10, 15, 12, 18]
Max of web-02: 95
City: Pune
First group: devops
Groups now: ['devops', 'docker', 'sudo']
```

**Example 2:**

```text
Region: ap-south-1
ID     NAME      TYPE       STATE    ENV
i-001  web-01    t3.micro   running  prod
i-002  batch-01  t3.large   stopped  dev
i-003  db-01     m5.xlarge  running  MISSING
Running instances: 2
Instances missing an Env tag: ['i-003']
Monitoring: disabled
```

## 8. Common Mistakes

**1. Mixing up list indexes and dict keys**

`inventory["instances"]["i-001"]` fails — `instances` is a list, so use a number index or loop.

**2. Long unreadable chains**

Store intermediate results: `tags = instance["tags"]` makes code easier to read and debug.

**3. Shared inner lists**

`[[0] * 3] * 3` creates three references to the SAME row. Use `[[0] * 3 for _ in range(3)]`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Classroom matrix:** Store marks of 3 students in 3 subjects as a nested list. Print the second student's marks, the third subject mark of the first student, and each student's total.
- **Task 2 (Medium) — Pod lookup:** Given `cluster = {"nodes": [{"name": "node-1", "pods": ["api-1", "api-2"]}, {"name": "node-2", "pods": ["db-0"]}]}`, print every pod with its node name, then the total number of pods.
- **Task 3 (Practical Challenge) — Student Information System (Project 1 preview):** Store students as a list of dicts with `name`, `age` and `marks` (a dict of subject → mark). For each student, print the average mark and a grade (A ≥ 85, B ≥ 70, C ≥ 50, F). Finally print the class topper.

## 10. DevOps/MLOps Connection

- **DevOps:** Kubernetes manifests (`spec.template.spec.containers[0].image`), Ansible inventories and Terraform state files are deeply nested.
- **Cloud:** boto3 responses (`Reservations → Instances → Tags`) require exactly today's navigation skills.
- **Data engineering:** flattening nested JSON into tables is a daily ETL job.
- **MLOps:** model registries and experiment trackers return nested metadata; prediction APIs accept nested JSON bodies.

## 11. Interview Questions

**Q1. How do you safely access a deeply nested optional key?**

<details><summary>Show answer</summary>

Chain `.get()` calls with empty-dict defaults, or wrap the access in try/except KeyError.

</details>

**Q2. Why is `[[0]*3]*3` a bug?**

<details><summary>Show answer</summary>

It repeats references to the same inner list, so changing one row changes all rows.

</details>

**Q3. How would you represent tabular data without Pandas?**

<details><summary>Show answer</summary>

As a list of dicts (one dict per row) or a list of lists/tuples with a header.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 28 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 027](../../03-dictionaries-logic/day-027/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 029 ➡](../../03-dictionaries-logic/day-029/README.md)
