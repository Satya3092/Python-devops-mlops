# Day 030 — While Loops

[⬅ Day 029](../../03-dictionaries-logic/day-029/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 031 ➡](../../03-dictionaries-logic/day-031/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Repeat code while a condition is True
- Avoid infinite loops with proper exit conditions
- Build retry and polling loops

## 2. Topic Explanation

A **while loop** repeats **as long as a condition is True**:

```python
attempt = 1
while attempt <= 3:
    print("Attempt", attempt)
    attempt += 1
```

- `for` = "do this for each item" (you know the collection).
- `while` = "keep doing this until something changes" (you don't know how many times).

Every while loop needs something inside it that eventually makes the condition False — otherwise you get an **infinite loop** (stop it with `Ctrl + C`).

`while True:` with a `break` inside is a common pattern for menus and polling.

DevOps uses: **retry until success**, **poll until a resource is ready** (`kubectl rollout status`), **wait until a port opens**.

## 3. Syntax

```python
while condition:
    body
    update_something_so_condition_changes

while True:
    if done:
        break
```

| Part | Meaning |
|---|---|
| `while` | Checks the condition before every iteration. |
| `condition` | Loop continues while it is True. |
| `update` | Changing a variable inside the loop so it eventually ends. |
| `break` | Exit the loop immediately (Day 32). |

## 4. Example 1 — Basic Example: Counting with while

```python
count = 5
while count > 0:
    print("Countdown:", count)
    count -= 1
print("Lift off!")

# Sum numbers until the total passes 20
total = 0
number = 1
while total <= 20:
    total += number
    number += 1
print("Total:", total, "after adding up to", number - 1)
```

## 5. Example 2 — Practical Example: Retry with exponential backoff and polling

```python
# Simulated health-check results: the service becomes healthy on the 4th try
health_results = [False, False, False, True]

MAX_ATTEMPTS = 5
attempt = 0
delay = 1
healthy = False

while attempt < MAX_ATTEMPTS and not healthy:
    healthy = health_results[attempt]
    attempt += 1
    if healthy:
        print(f"Attempt {attempt}: service is healthy")
    else:
        print(f"Attempt {attempt}: not ready, retrying in {delay}s")
        # time.sleep(delay)   # real code would wait here
        delay *= 2

if not healthy:
    print("Giving up after", MAX_ATTEMPTS, "attempts")

# Polling a rollout: replicas become ready one by one
desired_replicas = 3
ready_replicas = 0
checks = 0
while ready_replicas < desired_replicas:
    checks += 1
    ready_replicas += 1                 # simulate one pod becoming ready
    print(f"Check {checks}: {ready_replicas}/{desired_replicas} replicas ready")
print("Rollout complete")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `count -= 1` ensures the condition `count > 0` eventually becomes False.
- The second loop runs an unknown number of times — exactly when `while` is the right choice.

**Example 2**
- The retry loop stops when **either** the maximum attempts are reached **or** the service is healthy.
- `delay *= 2` implements exponential backoff (`time.sleep` is commented out so the example runs instantly).
- The polling loop mimics `kubectl rollout status`: keep checking until ready replicas equal desired replicas.

## 7. Expected Output

**Example 1:**

```text
Countdown: 5
Countdown: 4
Countdown: 3
Countdown: 2
Countdown: 1
Lift off!
Total: 21 after adding up to 6
```

**Example 2:**

```text
Attempt 1: not ready, retrying in 1s
Attempt 2: not ready, retrying in 2s
Attempt 3: not ready, retrying in 4s
Attempt 4: service is healthy
Check 1: 1/3 replicas ready
Check 2: 2/3 replicas ready
Check 3: 3/3 replicas ready
Rollout complete
```

## 8. Common Mistakes

**1. Infinite loops**

Forgetting `count -= 1` means the condition never changes. Always check what makes the loop end. Use `Ctrl + C` to stop a stuck program.

**2. Off-by-one errors**

`while i < 5` vs `while i <= 5` — decide whether the last value is included.

**3. Retry loops without a limit**

`while not healthy:` can wait forever. Always add a max attempts or timeout.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Sum of digits:** Use a while loop to compute the sum of the digits of 98765 (using `% 10` and `// 10`).
- **Task 2 (Medium) — Password prompt:** Ask for a password up to 3 times. The correct password is `devops123`. Print `Access granted` or, after 3 failures, `Account locked`.
- **Task 3 (Practical Challenge) — Queue consumer:** Simulate a message queue `["order-1", "order-2", "POISON", "order-3"]`. Process messages from the front with `while queue:`. If a message is `POISON`, move it to a dead-letter list instead of processing. Print processed and dead-letter lists.

## 10. DevOps/MLOps Connection

- **DevOps:** retry loops for flaky network calls, waiting for a database or port to be ready (`wait-for-it` scripts), polling CI jobs.
- **Cloud:** waiting until an EC2 instance is `running` or a CloudFormation stack completes (boto3 *waiters* use while loops internally).
- **Data engineering:** consuming messages from queues (SQS, Kafka) until the queue is empty.
- **ML:** training until a metric stops improving (early stopping).

## 11. Interview Questions

**Q1. When would you use while instead of for?**

<details><summary>Show answer</summary>

When the number of iterations is not known in advance — retrying, polling, reading until a condition changes.

</details>

**Q2. How do you avoid infinite loops in retry logic?**

<details><summary>Show answer</summary>

Limit attempts or total time, and make sure the condition can become False.

</details>

**Q3. What is exponential backoff and why use it?**

<details><summary>Show answer</summary>

Doubling the wait between retries; it reduces load on a struggling service and avoids thundering-herd problems.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 30 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 029](../../03-dictionaries-logic/day-029/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 031 ➡](../../03-dictionaries-logic/day-031/README.md)
