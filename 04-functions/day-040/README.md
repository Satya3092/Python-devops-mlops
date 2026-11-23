# Day 040 — Keyword Arguments

[⬅ Day 039](../../04-functions/day-039/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 041 ➡](../../04-functions/day-041/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Call functions using `name=value` keyword arguments
- Mix positional and keyword arguments correctly
- Force keyword-only parameters with `*`

## 2. Topic Explanation

**Keyword arguments** name the parameter you are filling:

```python
create_user(username="asha", group="devops", shell="/bin/bash")
```

Benefits:
- **Clarity:** `resize(width=800, height=600)` is clearer than `resize(800, 600)`.
- **Order doesn't matter:** `create_user(group="devops", username="asha")` works.
- **Skip defaults:** set only the options you need.

Rules:
- Positional arguments must come **before** keyword arguments in a call.
- You cannot give the same parameter twice.

**Keyword-only parameters:** everything after a bare `*` must be passed by name. Great for dangerous or confusing flags:
```python
def delete_bucket(name, *, force=False):
    ...
delete_bucket("logs", force=True)   # must be written explicitly
```

You use keyword arguments all the time already: `print(..., sep=",", end="")`.

## 3. Syntax

```python
function_name(param1=value1, param2=value2)
function_name(positional, keyword=value)

def function_name(a, b, *, flag=False):   # flag is keyword-only
    ...
```

| Part | Meaning |
|---|---|
| `name=value` | Keyword argument: matched by name, not position. |
| `positional first` | Positional arguments must precede keyword arguments. |
| `*` | In a definition, makes the following parameters keyword-only. |

## 4. Example 1 — Basic Example: Positional vs keyword calls

```python
def describe_pet(animal, name, age=1):
    return f"{name} is a {age}-year-old {animal}"


print(describe_pet("cat", "Milo"))
print(describe_pet(name="Bruno", animal="dog", age=4))
print(describe_pet("parrot", age=12, name="Rio"))

# describe_pet(name="Kitty", "cat")   # SyntaxError: positional argument follows keyword argument
```

## 5. Example 2 — Practical Example: Safe, self-documenting infrastructure helpers

```python
def create_instance(name, instance_type="t3.micro", *, region="us-east-1",
                    env="dev", monitoring=False, dry_run=True):
    """Describe an EC2 instance launch; region and flags are keyword-only."""
    mode = "DRY RUN" if dry_run else "LAUNCH"
    return (f"[{mode}] {name} type={instance_type} region={region} "
            f"env={env} monitoring={'on' if monitoring else 'off'}")


print(create_instance("web-01"))
print(create_instance("db-01", "m5.large", region="ap-south-1", env="prod", monitoring=True))
print(create_instance("batch-01", dry_run=False))

try:
    create_instance("web-02", "t3.small", "eu-west-1")   # region passed positionally
except TypeError as error:
    print("TypeError:", error)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The second and third calls pass arguments by name, so their order no longer matters.
- The commented-out last line would be a **syntax** error: a positional argument cannot follow a keyword argument. Python would refuse to run the whole file, so it is left as a comment (try un-commenting it to see the error).

**Example 2**
- `*` makes `region`, `env`, `monitoring` and `dry_run` keyword-only. Calls read like documentation.
- `dry_run=True` by default is a safety net: you must explicitly write `dry_run=False` to really launch something.
- Passing `"eu-west-1"` positionally raises `TypeError`, preventing a silent mistake.

## 7. Expected Output

**Example 1:**

```text
Milo is a 1-year-old cat
Bruno is a 4-year-old dog
Rio is a 12-year-old parrot
```

**Example 2:**

```text
[DRY RUN] web-01 type=t3.micro region=us-east-1 env=dev monitoring=off
[DRY RUN] db-01 type=m5.large region=ap-south-1 env=prod monitoring=on
[LAUNCH] batch-01 type=t3.micro region=us-east-1 env=dev monitoring=off
TypeError: create_instance() takes from 1 to 2 positional arguments but 3 were given
```

## 8. Common Mistakes

**1. Positional after keyword**

`f(name="x", 5)` → `SyntaxError: positional argument follows keyword argument`.

**2. Giving a value twice**

`f("cat", animal="dog")` → `TypeError: got multiple values for argument 'animal'`.

**3. Typos in names**

`f(animl="dog")` → `TypeError: unexpected keyword argument 'animl'`. Read the error message — it tells you the bad name.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Order a pizza:** Write `order_pizza(size, crust="thin", extra_cheese=False)` returning a description. Call it with keywords in a different order.
- **Task 2 (Medium) — Kubernetes scale command:** Write `scale_command(deployment, *, replicas, namespace="default")` that returns `kubectl scale deployment/<d> --replicas=<n> -n <ns>`. Show that calling it without `replicas=` raises a TypeError.
- **Task 3 (Practical Challenge) — Safe delete helper:** Write `delete_old_backups(backups, *, keep=3, dry_run=True)` where `backups` is a list of names sorted oldest→newest. It returns the list of backups it *would* delete and prints `Would delete ...` (dry run) or `Deleting ...`. Demonstrate both modes.

## 10. DevOps/MLOps Connection

- **DevOps:** `dry_run=True` defaults and keyword-only flags are best practice for destructive automation (deleting volumes, terminating instances).
- **Cloud:** boto3 requires keyword arguments for almost everything: `ec2.run_instances(ImageId=..., InstanceType=..., MinCount=1, MaxCount=1)`.
- **ML:** model constructors are configured with keyword args: `LogisticRegression(max_iter=1000, C=0.5)`.

## 11. Interview Questions

**Q1. What is the advantage of keyword arguments?**

<details><summary>Show answer</summary>

They make calls self-documenting, allow any order, and let you skip optional parameters.

</details>

**Q2. What does a bare `*` in a function signature do?**

<details><summary>Show answer</summary>

Every parameter after it must be passed as a keyword argument.

</details>

**Q3. Why do many cloud SDKs require keyword arguments?**

<details><summary>Show answer</summary>

APIs have many optional parameters; names prevent ordering mistakes and allow the API to evolve without breaking callers.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 40 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 039](../../04-functions/day-039/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 041 ➡](../../04-functions/day-041/README.md)
